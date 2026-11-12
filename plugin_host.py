"""Small V1 capability host with metadata-only discovery and lazy plugin loading."""
from __future__ import annotations
import importlib
import json
import sys
from pathlib import Path
from typing import Any

class PluginHostError(RuntimeError):
    pass

class PluginHost:
    def __init__(self, index_path: str | Path = "registry/index.json"):
        self.index_path = Path(index_path).resolve()
        self._index = json.loads(self.index_path.read_text(encoding="utf-8"))
        self._loaded = {}

    def discover(self, capability: str, extension: str | None = None) -> list[dict[str, Any]]:
        found = []
        for item in self._index.get("plugins", []):
            if extension and extension.lower() not in [x.lower() for x in item.get("supported_extensions", [])]:
                continue
            for cap in item.get("capabilities", []):
                if cap.get("id") == capability:
                    found.append({"plugin_id": item["id"], "name": item["name"],
                                  "description": item["description"], "capability": cap})
        return found

    def _load(self, plugin_id: str):
        if plugin_id in self._loaded:
            return self._loaded[plugin_id]
        entry = next((p for p in self._index.get("plugins", []) if p["id"] == plugin_id), None)
        if not entry:
            raise PluginHostError(f"Unknown plugin: {plugin_id}")
        root = (self.index_path.parent.parent / entry["path"]).resolve()
        if not root.is_dir():
            raise PluginHostError(f"Plugin directory not found: {root}")
        module_name, function_name = entry["entry_point"].split(":", 1)
        sys.path.insert(0, str(root))
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
        except Exception:
            if sys.path and sys.path[0] == str(root):
                sys.path.pop(0)
            raise
        self._loaded[plugin_id] = function
        return function

    def execute(self, capability: str, **params) -> dict[str, Any]:
        matches = self.discover(capability)
        if len(matches) != 1:
            return {"success": False, "errors": [{"code": "capability_not_unique",
                    "message": f"Expected one provider for {capability}; found {len(matches)}"}]}
        selected = matches[0]
        entry = next(p for p in self._index["plugins"] if p["id"] == selected["plugin_id"])
        if selected["capability"].get("mode") != "read":
            return {"success": False, "errors": [{"code": "policy_denied",
                    "message": "This reconstructed host only permits read capabilities."}]}
        try:
            fn = self._load(entry["id"])
            return fn(selected["capability"]["action"], params)
        except Exception as exc:
            return {"success": False, "plugin": entry["id"],
                    "errors": [{"code": "execution_error", "message": str(exc)}]}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ECU SOFT Agent Plugin Host")
    parser.add_argument("--list", action="store_true", help="List registered plugins and capabilities")
    parser.add_argument("--discover", metavar="CAPABILITY", help="Discover a capability")
    parser.add_argument("--extension", default=None, help="Optional file extension filter, e.g. .bin")
    args = parser.parse_args()
    host = PluginHost()
    if args.list:
        for item in host._index.get("plugins", []):
            print(f"{item['id']} v{item['version']} - {item['name']}")
            for cap in item.get("capabilities", []):
                print(f"  {cap['id']}: {cap['description']}")
    elif args.discover:
        print(json.dumps(host.discover(args.discover, args.extension), ensure_ascii=False, indent=2))
    else:
        parser.print_help()
