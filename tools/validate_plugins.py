from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
seen = set()
for p in (ROOT / "plugins").rglob("plugin.json"):
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
        for key in ("id","name","version","description","category","supported_extensions","entry_point","capabilities"):
            if key not in m: errors.append(f"{p}: missing {key}")
        if m.get("id") in seen: errors.append(f"{p}: duplicate plugin id {m.get('id')}")
        seen.add(m.get("id"))
        if not isinstance(m.get("capabilities"), list) or not m["capabilities"]:
            errors.append(f"{p}: capabilities must be a non-empty list")
        for c in m.get("capabilities", []):
            for key in ("id","action","description","mode"):
                if key not in c: errors.append(f"{p}: capability missing {key}")
    except Exception as exc:
        errors.append(f"{p}: {exc}")
if errors:
    print("\\n".join(errors)); sys.exit(1)
print(f"Validated {len(seen)} plugin(s)")
