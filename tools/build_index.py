"""Build all registry indexes from plugin.json manifests."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / "plugins"
REGISTRY_DIR = ROOT / "registry"


def load_manifest(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["id", "name", "version", "description", "category",
                "operations", "capabilities", "file_extensions", "entry_point"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"{path}: missing fields {missing}")
    if not isinstance(data["operations"], list) or not data["operations"]:
        raise ValueError(f"{path}: operations must be a non-empty list")
    if not isinstance(data["capabilities"], list):
        raise ValueError(f"{path}: capabilities must be a list")
    root = path.parent.relative_to(ROOT).as_posix()
    entry = path.parent / data["entry_point"]
    if not entry.is_file():
        raise ValueError(f"{path}: entry point missing: {data['entry_point']}")
    data["_root"] = root
    data["_entry"] = data["entry_point"]
    data["_sha256"] = hashlib.sha256(entry.read_bytes()).hexdigest()
    return data


def write_json(name, value):
    target = REGISTRY_DIR / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    manifests = sorted(PLUGINS_DIR.rglob("plugin.json"))
    records = [load_manifest(path) for path in manifests]
    ids = [item["id"] for item in records]
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates:
        raise SystemExit(f"Duplicate plugin IDs: {duplicates}")

    index_plugins = []
    capabilities, operations, file_types, categories = {}, {}, {}, {}
    dependencies, versions, integrity = {}, {}, {}

    for item in records:
        pid = item["id"]
        for cap in item["capabilities"]:
            capabilities.setdefault(cap, []).append(pid)
        for op in item["operations"]:
            operations.setdefault(op, []).append(pid)
        for ext in item["file_extensions"]:
            file_types.setdefault(ext.lower(), []).append(pid)
        categories.setdefault(item["category"], []).append(pid)
        dependencies[pid] = item.get("dependencies", [])
        versions[pid] = {
            "version": item["version"],
            "api_compatibility": item.get("api_compatibility", "1.x")
        }
        integrity[pid] = {"entry_point_sha256": item["_sha256"]}
        index_plugins.append({
            "id": pid, "name": item["name"], "version": item["version"],
            "description": item["description"], "category": item["category"],
            "status": item.get("status", "active"),
            "trust": item.get("trust", "untrusted"),
            "root": item["_root"], "entry_point": item["_entry"],
            "operations": item["operations"],
            "capabilities": item["capabilities"],
            "file_extensions": item["file_extensions"],
            "permissions": item.get("permissions", []),
            "context": item.get("context", {}),
            "sha256": item["_sha256"]
        })

    write_json("index.json", {"registry_version": "1.0.0",
                              "generated_by": "tools/build_index.py",
                              "plugins": index_plugins})
    for name, value in [
        ("capabilities.json", capabilities), ("operations.json", operations),
        ("file_types.json", file_types), ("categories.json", categories),
        ("dependencies.json", dependencies), ("versions.json", versions),
        ("integrity.json", {"algorithm": "sha256", "plugins": integrity})
    ]:
        write_json(name, value)
    print(f"Registry built successfully: {len(index_plugins)} plugin(s), {len(manifests)} manifest(s).")


if __name__ == "__main__":
    main()
