"""Human-readable registry summary."""
import json
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "registry" / "index.json"
data = json.loads(p.read_text(encoding="utf-8"))
print(f"Registry version: {data.get('registry_version')}")
for item in data.get("plugins", []):
    print(f"- {item['id']} [{item['status']}]")
    print(f"  Operations: {', '.join(item['operations'])}")
    print(f"  Extensions: {', '.join(item['file_extensions'])}")
