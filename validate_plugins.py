from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];errors=[];seen=set()
for p in (ROOT/"plugins").rglob("plugin.json"):
 try:
  m=json.loads(p.read_text(encoding="utf-8"))
  for k in ("id","name","version","description","category","supported_extensions","entry_point","capabilities"):
   if k not in m:errors.append(f"{p}: missing {k}")
  if m.get("id") in seen:errors.append(f"{p}: duplicate plugin id")
  seen.add(m.get("id"))
  if not isinstance(m.get("capabilities"),list) or not m["capabilities"]:errors.append(f"{p}: empty capabilities")
  for c in m.get("capabilities",[]):
   for k in ("id","action","description","mode"):
    if k not in c:errors.append(f"{p}: capability missing {k}")
 except Exception as e:errors.append(f"{p}: {e}")
if errors:print("\n".join(errors));sys.exit(1)
print(f"Validated {len(seen)} plugin(s)")
