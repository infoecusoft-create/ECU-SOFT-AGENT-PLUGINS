from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
plugins = []
for manifest_path in sorted((ROOT / "plugins").rglob("plugin.json")):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rel = manifest_path.parent.relative_to(ROOT).as_posix()
    plugins.append({
        "id": manifest["id"], "name": manifest["name"], "version": manifest["version"],
        "description": manifest["description"], "category": manifest["category"],
        "supported_extensions": manifest["supported_extensions"],
        "entry_point": manifest["entry_point"], "capabilities": manifest["capabilities"],
        "path": rel, "trust": manifest.get("trust", "untrusted")
    })
out = ROOT / "registry" / "index.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({"schema_version": 1, "plugins": plugins}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Indexed {len(plugins)} plugin(s) -> {out.relative_to(ROOT)}")
