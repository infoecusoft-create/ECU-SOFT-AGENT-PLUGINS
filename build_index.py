from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];plugins=[]
for manifest_path in sorted((ROOT/"plugins").rglob("plugin.json")):
 m=json.loads(manifest_path.read_text(encoding="utf-8"));rel=manifest_path.parent.relative_to(ROOT).as_posix()
 plugins.append({"id":m["id"],"name":m["name"],"version":m["version"],"description":m["description"],"category":m["category"],"supported_extensions":m["supported_extensions"],"entry_point":m["entry_point"],"capabilities":m["capabilities"],"path":rel,"trust":m.get("trust","untrusted")})
out=ROOT/"registry/index.json";out.parent.mkdir(exist_ok=True);out.write_text(json.dumps({"schema_version":1,"plugins":plugins},ensure_ascii=False,indent=2),encoding="utf-8");print(f"Indexed {len(plugins)} plugin(s)")
