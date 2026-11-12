"""Validate plugin manifests and their entry points."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
errors = []
seen = set()
for manifest in sorted((ROOT / "plugins").rglob("plugin.json")):
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for key in ("id", "name", "version", "description", "category",
                    "operations", "capabilities", "file_extensions", "entry_point"):
            if key not in data:
                errors.append(f"{manifest}: missing {key}")
        pid = data.get("id")
        if pid in seen:
            errors.append(f"{manifest}: duplicate id {pid}")
        seen.add(pid)
        if not (manifest.parent / data.get("entry_point", "")).is_file():
            errors.append(f"{manifest}: missing entry point")
    except Exception as exc:
        errors.append(f"{manifest}: {exc}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"Validation successful: {len(seen)} plugin(s).")
