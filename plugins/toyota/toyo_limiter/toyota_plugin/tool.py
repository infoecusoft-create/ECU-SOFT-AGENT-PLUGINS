"""Read-only Toyota BIN inspection extracted from the supplied TOYO LIMITER source.

This module deliberately does not modify ECU binaries. It identifies profile candidates
and reports source-derived offsets/raw bytes for engineering review.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

_DATA = Path(__file__).with_name("profiles.json")
MAX_FILE_SIZE = 16 * 1024 * 1024

class PluginError(ValueError):
    """Expected plugin input or profile error."""

def _load_profiles() -> list[dict[str, Any]]:
    payload = json.loads(_DATA.read_text(encoding="utf-8"))
    return payload["profiles"]

def _pattern(value: str | None) -> bytes:
    if not value:
        return b""
    try:
        return bytes.fromhex(value)
    except ValueError as exc:
        raise PluginError(f"Invalid hex pattern in profile data: {value!r}") from exc

def _all_offsets(blob: bytes, needle: bytes) -> list[int]:
    if not needle:
        return []
    out, pos = [], 0
    while True:
        pos = blob.find(needle, pos)
        if pos < 0:
            return out
        out.append(pos)
        pos += 1

def _validate_file(file_path: str | Path) -> tuple[Path, bytes]:
    path = Path(file_path).expanduser()
    if not path.is_file():
        raise PluginError(f"Input file does not exist or is not a file: {path}")
    size = path.stat().st_size
    if size <= 0 or size > MAX_FILE_SIZE:
        raise PluginError(f"File size must be between 1 and {MAX_FILE_SIZE} bytes; got {size}")
    if path.suffix.lower() != ".bin":
        raise PluginError("Only .bin files are accepted")
    return path, path.read_bytes()

def _profile_candidates(blob: bytes) -> list[dict[str, Any]]:
    size = len(blob)
    candidates = []
    for profile in _load_profiles():
        if profile.get("EXPECTED_SIZE") != size:
            continue
        pattern = _pattern(profile.get("PATTERN_START"))
        offsets = _all_offsets(blob, pattern)
        candidates.append({"profile": profile, "pattern_offsets": offsets})
    return candidates

def identify_vehicle(file_path: str | Path) -> dict[str, Any]:
    """Return size/pattern-based candidates; ambiguous matches are never guessed."""
    path, blob = _validate_file(file_path)
    candidates = _profile_candidates(blob)
    if not candidates:
        return {"identified": False, "status": "unsupported_size", "file": path.name,
                "size": len(blob), "candidates": [], "message": "No source profile has this exact file size."}
    matched = [c for c in candidates if c["pattern_offsets"]]
    # A source key duplicated with conflicting sizes is kept as separate variants and flagged.
    unique_profiles = [c for c in matched]
    if len(unique_profiles) == 1 and not unique_profiles[0]["profile"].get("_source_conflict"):
        c = unique_profiles[0]
        return {"identified": True, "status": "pattern_match", "file": path.name,
                "size": len(blob), "profile_id": c["profile"]["id"],
                "source_name": c["profile"]["source_name"],
                "pattern_offsets": c["pattern_offsets"], "confidence": "pattern_confirmed"}
    summaries = []
    for c in candidates:
        p=c["profile"]
        summaries.append({"profile_id":p["id"],"source_name":p["source_name"],
                          "pattern_offsets":c["pattern_offsets"],
                          "source_conflict":bool(p.get("_source_conflict"))})
    status = "ambiguous" if matched else "size_only"
    return {"identified": False, "status": status, "file": path.name,
            "size": len(blob), "candidates": summaries,
            "message": "Profile cannot be selected uniquely from the source evidence; no profile was guessed."}

def _read_rpm(blob: bytes, profile: dict[str, Any]) -> dict[str, Any] | None:
    start_pat=_pattern(profile.get("RPM_PATTERN_START")); end_pat=_pattern(profile.get("RPM_PATTERN_END"))
    if not start_pat or not end_pat:
        return None
    starts=_all_offsets(blob,start_pat); ends=_all_offsets(blob,end_pat)
    pairs=[(s,e) for s in starts for e in ends if e > s + len(start_pat)]
    if len(pairs) != 1:
        return {"available":False,"reason":"missing_or_ambiguous_delimiters",
                "start_offsets":starts,"end_offsets":ends}
    s,e=pairs[0]; offset=s+len(start_pat)
    if offset+2 > e:
        return {"available":False,"reason":"insufficient_bytes_between_delimiters"}
    raw=blob[offset:offset+2]
    return {"available":True,"offset":offset,"raw_hex":raw.hex(" "),
            "little_endian_u16_observed":int.from_bytes(raw,"little"),
            "region_length":e-offset}

def _cut_count(profile: dict[str, Any]) -> int:
    name=profile.get("source_name","")
    if name == "forchenar_GIN1": return 6
    if name in ("Shas_GIN1","Shas_GIN2"): return 8
    if name == "tndra_GIN1_2": return 4
    return 7

def inspect_bin(file_path: str | Path) -> dict[str, Any]:
    """Inspect a BIN and return source-derived observations only; never writes the file."""
    path, blob = _validate_file(file_path)
    ident=identify_vehicle(path)
    if not ident.get("identified"):
        return {"success":False,"identification":ident,"analysis":None,
                "sha256":hashlib.sha256(blob).hexdigest(),"read_only":True}
    profile=next(p for p in _load_profiles() if p["id"]==ident["profile_id"])
    speed_pat=_pattern(profile.get("PATTERN_START"))
    speed_matches=_all_offsets(blob,speed_pat)
    if len(speed_matches)!=1:
        return {"success":False,"identification":ident,
                "error":"speed_anchor_missing_or_ambiguous","speed_anchor_offsets":speed_matches,
                "sha256":hashlib.sha256(blob).hexdigest(),"read_only":True}
    speed_offset=speed_matches[0]+len(speed_pat)
    speed_len=int(profile.get("SPEED_LENGTH",16))
    if speed_len<=0 or speed_offset+speed_len>len(blob):
        raise PluginError("Speed data range falls outside the input file")
    speed_raw=blob[speed_offset:speed_offset+speed_len]
    rpm=_read_rpm(blob,profile)
    cut_pat=_pattern(profile.get("CUT_PATTERN"))
    cut_info=None
    if cut_pat:
        cut_matches=_all_offsets(blob,cut_pat)
        if len(cut_matches)==1:
            offset=cut_matches[0]+len(cut_pat); count=_cut_count(profile)
            end=offset+count*2
            if end<=len(blob):
                vals=[int.from_bytes(blob[offset+i*2:offset+i*2+2],"little") for i in range(count)]
                cut_info={"available":True,"offset":offset,"count":count,
                          "raw_hex":blob[offset:end].hex(" "),"observed_u16_values":vals,
                          "source_heuristic_status":"uniform_values" if len(set(vals))==1 else "non_uniform_values"}
            else: cut_info={"available":False,"reason":"cut_data_out_of_bounds"}
        else: cut_info={"available":False,"reason":"cut_anchor_missing_or_ambiguous","anchor_offsets":cut_matches}
    return {"success":True,"read_only":True,"file":path.name,"size":len(blob),
            "sha256":hashlib.sha256(blob).hexdigest(),"identification":ident,
            "analysis":{"profile_id":profile["id"],"source_name":profile["source_name"],
                "speed":{"available":True,"offset":speed_offset,"length":speed_len,
                         "raw_hex":speed_raw.hex(" "),"observed_bytes":list(speed_raw),
                         "note":"Source code displays max(raw bytes); no physical conversion is inferred."},
                "rpm":rpm,"cut_off":cut_info},
            "limitations":["Read-only inspection; no ECU data is modified.",
                "Values are reported as raw/source-derived observations, not validated calibration units.",
                "A unique size and pattern match does not prove ECU compatibility or safe calibration."]}

def execute(action: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Simple adapter; map this to the repository's actual PluginHost contract."""
    params=params or {}
    try:
        if action == "identify_vehicle": result=identify_vehicle(params["file_path"])
        elif action in ("inspect_bin","inspect_speed","inspect_rpm","inspect_cutoff"):
            # The source performs a combined inspection; return only its safe report.
            result=inspect_bin(params["file_path"])
            if action != "inspect_bin" and result.get("success"):
                result={"success":True,"read_only":True,"identification":result["identification"],
                        "analysis":{action.removeprefix("inspect_"):result["analysis"].get(
                            {"speed":"speed","rpm":"rpm","cutoff":"cut_off"}[action.removeprefix("inspect_")])}}
        else:
            return {"success":False,"plugin":"toyo_limiter","action":action,
                    "errors":[{"code":"unsupported_action","message":f"Unsupported read-only action: {action}"}]}
        return {"success":True,"plugin":"toyo_limiter","action":action,"data":result,"errors":[]}
    except (PluginError, KeyError, OSError) as exc:
        return {"success":False,"plugin":"toyo_limiter","action":action,
                "errors":[{"code":"invalid_input_or_analysis_error","message":str(exc)}]}
