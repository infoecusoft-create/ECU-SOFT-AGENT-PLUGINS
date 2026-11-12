"""Read-only Toyota BIN inspection extracted from the supplied TOYO LIMITER source.

This preserved file is the exact source text fetched from the repository for this task.
It deliberately does not modify ECU binaries.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any
_DATA=Path(__file__).with_name("profiles.json")
MAX_FILE_SIZE=16*1024*1024
class PluginError(ValueError): pass
def _load_profiles()->list[dict[str,Any]]:return json.loads(_DATA.read_text(encoding="utf-8"))["profiles"]
def _pattern(value:str|None)->bytes:
 if not value:return b""
 try:return bytes.fromhex(value)
 except ValueError as exc:raise PluginError(f"Invalid hex pattern in profile data: {value!r}") from exc
def _all_offsets(blob:bytes,needle:bytes)->list[int]:
 if not needle:return []
 out=[];pos=0
 while True:
  pos=blob.find(needle,pos)
  if pos<0:return out
  out.append(pos);pos+=1
def _validate_file(file_path:str|Path)->tuple[Path,bytes]:
 path=Path(file_path).expanduser()
 if not path.is_file():raise PluginError(f"Input file does not exist or is not a file: {path}")
 size=path.stat().st_size
 if size<=0 or size>MAX_FILE_SIZE:raise PluginError(f"File size must be between 1 and {MAX_FILE_SIZE} bytes; got {size}")
 if path.suffix.lower()!=".bin":raise PluginError("Only .bin files are accepted")
 return path,path.read_bytes()
def _profile_candidates(blob:bytes)->list[dict[str,Any]]:
 return [{"profile":p,"pattern_offsets":_all_offsets(blob,_pattern(p.get("PATTERN_START")))} for p in _load_profiles() if p.get("EXPECTED_SIZE")==len(blob)]
def identify_vehicle(file_path:str|Path)->dict[str,Any]:
 path,blob=_validate_file(file_path);candidates=_profile_candidates(blob)
 if not candidates:return {"identified":False,"status":"unsupported_size","file":path.name,"size":len(blob),"candidates":[],"message":"No source profile has this exact file size."}
 matched=[c for c in candidates if c["pattern_offsets"]]
 if len(matched)==1 and not matched[0]["profile"].get("_source_conflict"):
  c=matched[0];return {"identified":True,"status":"pattern_match","file":path.name,"size":len(blob),"profile_id":c["profile"]["id"],"source_name":c["profile"]["source_name"],"pattern_offsets":c["pattern_offsets"],"confidence":"pattern_confirmed"}
 return {"identified":False,"status":"ambiguous" if matched else "size_only","file":path.name,"size":len(blob),"candidates":[{"profile_id":c["profile"]["id"],"source_name":c["profile"]["source_name"],"pattern_offsets":c["pattern_offsets"],"source_conflict":bool(c["profile"].get("_source_conflict"))} for c in candidates],"message":"Profile cannot be selected uniquely from the source evidence; no profile was guessed."}
def _read_rpm(blob:bytes,p:dict[str,Any])->dict[str,Any]|None:
 a=_pattern(p.get("RPM_PATTERN_START"));b=_pattern(p.get("RPM_PATTERN_END"))
 if not a or not b:return None
 starts=_all_offsets(blob,a);ends=_all_offsets(blob,b);pairs=[(s,e) for s in starts for e in ends if e>s+len(a)]
 if len(pairs)!=1:return {"available":False,"reason":"missing_or_ambiguous_delimiters","start_offsets":starts,"end_offsets":ends}
 s,e=pairs[0];off=s+len(a)
 if off+2>e:return {"available":False,"reason":"insufficient_bytes_between_delimiters"}
 raw=blob[off:off+2];return {"available":True,"offset":off,"raw_hex":raw.hex(" "),"little_endian_u16_observed":int.from_bytes(raw,"little"),"region_length":e-off}
def _cut_count(p:dict[str,Any])->int:
 n=p.get("source_name","")
 if n=="forchenar_GIN1":return 6
 if n in ("Shas_GIN1","Shas_GIN2"):return 8
 if n=="tndra_GIN1_2":return 4
 return 7
def inspect_bin(file_path:str|Path)->dict[str,Any]:
 path,blob=_validate_file(file_path);ident=identify_vehicle(path);sha=hashlib.sha256(blob).hexdigest()
 if not ident.get("identified"):return {"success":False,"identification":ident,"analysis":None,"sha256":sha,"read_only":True}
 p=next(p for p in _load_profiles() if p["id"]==ident["profile_id"]);sp=_pattern(p.get("PATTERN_START"));hits=_all_offsets(blob,sp)
 if len(hits)!=1:return {"success":False,"identification":ident,"error":"speed_anchor_missing_or_ambiguous","speed_anchor_offsets":hits,"sha256":sha,"read_only":True}
 off=hits[0]+len(sp);n=int(p.get("SPEED_LENGTH",16))
 if n<=0 or off+n>len(blob):raise PluginError("Speed data range falls outside the input file")
 raw=blob[off:off+n];rpm=_read_rpm(blob,p);cp=_pattern(p.get("CUT_PATTERN"));cut=None
 if cp:
  hits=_all_offsets(blob,cp)
  if len(hits)==1:
   co=hits[0]+len(cp);count=_cut_count(p);end=co+count*2
   if end<=len(blob):
    vals=[int.from_bytes(blob[co+i*2:co+i*2+2],"little") for i in range(count)];cut={"available":True,"offset":co,"count":count,"raw_hex":blob[co:end].hex(" "),"observed_u16_values":vals,"source_heuristic_status":"uniform_values" if len(set(vals))==1 else "non_uniform_values"}
   else:cut={"available":False,"reason":"cut_data_out_of_bounds"}
  else:cut={"available":False,"reason":"cut_anchor_missing_or_ambiguous","anchor_offsets":hits}
 return {"success":True,"read_only":True,"file":path.name,"size":len(blob),"sha256":sha,"identification":ident,"analysis":{"profile_id":p["id"],"source_name":p["source_name"],"speed":{"available":True,"offset":off,"length":n,"raw_hex":raw.hex(" "),"observed_bytes":list(raw),"note":"Source code displays max(raw bytes); no physical conversion is inferred."},"rpm":rpm,"cut_off":cut},"limitations":["Read-only inspection; no ECU data is modified.","Values are reported as raw/source-derived observations, not validated calibration units.","A unique size and pattern match does not prove ECU compatibility or safe calibration."]}
def execute(action:str,params:dict[str,Any]|None=None)->dict[str,Any]:
 params=params or {}
 try:
  if action=="identify_vehicle":result=identify_vehicle(params["file_path"])
  elif action in ("inspect_bin","inspect_speed","inspect_rpm","inspect_cutoff"):
   result=inspect_bin(params["file_path"])
   if action!="inspect_bin" and result.get("success"):
    key={"speed":"speed","rpm":"rpm","cutoff":"cut_off"}[action.removeprefix("inspect_")];result={"success":True,"read_only":True,"identification":result["identification"],"analysis":{key:result["analysis"].get(key)}}
  else:return {"success":False,"plugin":"toyo_limiter","action":action,"errors":[{"code":"unsupported_action","message":f"Unsupported read-only action: {action}"}]}
  return {"success":True,"plugin":"toyo_limiter","action":action,"data":result,"errors":[]}
 except (PluginError,KeyError,OSError) as exc:return {"success":False,"plugin":"toyo_limiter","action":action,"errors":[{"code":"invalid_input_or_analysis_error","message":str(exc)}]}
