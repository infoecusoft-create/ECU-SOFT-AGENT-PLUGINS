"""
ECU-SOFT-AGENT-PLUGINS — single-file Plugin Host core (V1).

Discovery reads registry metadata only. Plugin Python modules are imported only
after a plugin has been resolved and execution has passed basic policy checks.
This is a starter implementation, not a hardened sandbox.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import time
from pathlib import Path
from typing import Any


class PluginHostError(Exception):
    code = "PLUGIN_HOST_ERROR"

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def as_dict(self):
        return {"code": self.code, "message": self.message, "details": self.details}


class PluginNotFoundError(PluginHostError):
    code = "PLUGIN_NOT_FOUND"


class OperationNotSupportedError(PluginHostError):
    code = "OPERATION_NOT_SUPPORTED"


class InvalidInputError(PluginHostError):
    code = "INVALID_INPUT"


class PermissionDeniedError(PluginHostError):
    code = "PERMISSION_DENIED"


class IntegrityError(PluginHostError):
    code = "INTEGRITY_CHECK_FAILED"


class PluginExecutionError(PluginHostError):
    code = "PLUGIN_EXECUTION_FAILED"


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PluginHostError(f"Required JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PluginHostError(f"Invalid JSON in {path}: {exc}") from exc


def _safe_relative_path(base: Path, relative: str) -> Path:
    candidate = (base / relative).resolve()
    base_resolved = base.resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise PermissionDeniedError("Path escapes the repository/plugin directory.")
    return candidate


class PluginHost:
    """Metadata-driven plugin discovery and lazy execution host."""

    def __init__(self, registry_path: str | Path = "registry/index.json",
                 allow_untrusted: bool = False):
        self.registry_path = Path(registry_path).resolve()
        self.repository_root = self.registry_path.parent.parent
        self.allow_untrusted = allow_untrusted
        self._loaded: dict[str, Any] = {}
        self.registry = _read_json(self.registry_path)
        self.plugins = {
            item["id"]: item for item in self.registry.get("plugins", [])
        }

    def refresh(self):
        self.registry = _read_json(self.registry_path)
        self.plugins = {
            item["id"]: item for item in self.registry.get("plugins", [])
        }

    def discover(self, operation: str | None = None,
                 extension: str | None = None,
                 required_capabilities: list[str] | None = None,
                 context: dict | None = None) -> list[dict]:
        """Return matching metadata. This method never imports plugin code."""
        context = context or {}
        required_capabilities = set(required_capabilities or [])
        ext = extension.lower() if extension else None
        matches = []

        for plugin in self.plugins.values():
            if plugin.get("status", "active") != "active":
                continue
            operations = set(plugin.get("operations", []))
            capabilities = set(plugin.get("capabilities", []))
            extensions = {x.lower() for x in plugin.get("file_extensions", [])}

            if operation and operation not in operations:
                continue
            if ext and ext not in extensions:
                continue
            if not required_capabilities.issubset(capabilities):
                continue

            score = 0
            reasons = []
            if operation:
                score += 35
                reasons.append("operation match")
            if required_capabilities:
                score += 25
                reasons.append("capability match")
            if ext:
                score += 15
                reasons.append("file type match")

            plugin_context = plugin.get("context", {})
            requested_vehicle = context.get("vehicle")
            supported_vehicles = plugin_context.get("vehicles", [])
            if requested_vehicle and supported_vehicles:
                if requested_vehicle not in supported_vehicles:
                    continue
                score += 15
                reasons.append("vehicle context match")

            matches.append({
                **plugin,
                "match_score": score,
                "match_reasons": reasons
            })

        return sorted(matches, key=lambda item: (-item["match_score"], item["id"]))

    def inspect_plugin(self, plugin_id: str) -> dict:
        plugin = self.plugins.get(plugin_id)
        if not plugin:
            raise PluginNotFoundError(f"Plugin not found: {plugin_id}")
        return dict(plugin)

    def _verify_integrity(self, plugin: dict, entry_path: Path):
        expected = plugin.get("sha256")
        if not expected:
            return
        actual = hashlib.sha256(entry_path.read_bytes()).hexdigest()
        if actual.lower() != expected.lower():
            raise IntegrityError(
                "Plugin entry-point hash does not match registry metadata.",
                {"plugin_id": plugin["id"], "expected": expected, "actual": actual}
            )

    def _load(self, plugin: dict):
        plugin_id = plugin["id"]
        if plugin_id in self._loaded:
            return self._loaded[plugin_id]

        trust = plugin.get("trust", "untrusted")
        if trust != "trusted" and not self.allow_untrusted:
            raise PermissionDeniedError(
                "Plugin is untrusted. Review it and explicitly enable untrusted plugins.",
                {"plugin_id": plugin_id}
            )

        plugin_root = self.repository_root / plugin["root"]
        entry = _safe_relative_path(plugin_root, plugin["entry_point"])
        if not entry.is_file():
            raise PluginNotFoundError("Plugin entry point does not exist.",
                                      {"path": str(entry)})

        self._verify_integrity(plugin, entry)
        module_name = "ecu_plugin_" + re.sub(r"[^a-zA-Z0-9_]", "_", plugin_id)
        spec = importlib.util.spec_from_file_location(module_name, entry)
        if spec is None or spec.loader is None:
            raise PluginHostError("Could not create an import specification.")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        factory = getattr(module, "create_plugin", None)
        if not callable(factory):
            raise PluginHostError("Plugin must expose create_plugin().")
        instance = factory()
        self._loaded[plugin_id] = instance
        return instance

    def execute(self, operation: str, file_path: str | Path | None = None,
                inputs: dict | None = None, context: dict | None = None,
                plugin_id: str | None = None,
                approved_permissions: list[str] | None = None) -> dict:
        """Resolve, authorize, lazy-load and execute one operation."""
        inputs = dict(inputs or {})
        context = dict(context or {})
        approved_permissions = set(approved_permissions or [])
        started = time.perf_counter()

        if file_path is not None:
            path = Path(file_path).expanduser().resolve()
            if not path.is_file():
                raise InvalidInputError("Input file does not exist.",
                                         {"file_path": str(path)})
            inputs.setdefault("file_path", str(path))
            extension = path.suffix.lower()
        else:
            extension = inputs.get("extension")

        if plugin_id:
            plugin = self.plugins.get(plugin_id)
            if not plugin:
                raise PluginNotFoundError(f"Plugin not found: {plugin_id}")
            if operation not in plugin.get("operations", []):
                raise OperationNotSupportedError(
                    f"{plugin_id} does not support {operation}."
                )
        else:
            candidates = self.discover(
                operation=operation, extension=extension,
                context=context
            )
            if not candidates:
                raise PluginNotFoundError(
                    "No active plugin matches the requested operation and file type.",
                    {"operation": operation, "extension": extension}
                )
            plugin = candidates[0]

        permissions = set(plugin.get("permissions", []))
        missing = permissions - approved_permissions
        if missing:
            raise PermissionDeniedError(
                "Required permissions were not explicitly approved.",
                {"required": sorted(permissions), "missing": sorted(missing)}
            )

        instance = self._load(plugin)
        if not callable(getattr(instance, "execute", None)):
            raise PluginHostError("Plugin instance has no execute() method.")

        try:
            output = instance.execute(operation, inputs, context=context)
        except PluginHostError:
            raise
        except Exception as exc:
            raise PluginExecutionError(str(exc), {"plugin_id": plugin["id"]}) from exc

        return {
            "success": True,
            "plugin_id": plugin["id"],
            "operation": operation,
            "output": output if isinstance(output, dict) else {"value": output},
            "artifacts": [],
            "warnings": [],
            "errors": [],
            "execution_time_ms": round((time.perf_counter() - started) * 1000, 3)
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ECU SOFT Plugin Host")
    parser.add_argument("--registry", default="registry/index.json")
    parser.add_argument("--list", action="store_true", help="List registered plugins")
    parser.add_argument("--discover", metavar="OPERATION")
    parser.add_argument("--extension", default=None)
    args = parser.parse_args()

    host = PluginHost(args.registry)
    if args.list:
        print(json.dumps(list(host.plugins.values()), indent=2))
    elif args.discover:
        print(json.dumps(host.discover(args.discover, args.extension), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
