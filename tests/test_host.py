import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from plugin_host import PluginHost, PermissionDeniedError


def test_discovery_uses_registry_metadata():
    host = PluginHost(ROOT / "registry" / "index.json")
    found = host.discover("inspect_binary", ".bin")
    assert found
    assert found[0]["id"] == "example.binary.inspector"


def test_discovery_does_not_load_plugin():
    host = PluginHost(ROOT / "registry" / "index.json")
    host.discover("inspect_binary", ".bin")
    assert "example.binary.inspector" not in host._loaded


def test_untrusted_plugin_requires_explicit_opt_in(tmp_path):
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"\x01\x02\x03")
    host = PluginHost(ROOT / "registry" / "index.json")
    try:
        host.execute("inspect_binary", file_path=sample)
    except PermissionDeniedError:
        pass
    else:
        raise AssertionError("Untrusted plugin should not execute by default")


def test_example_plugin_executes_when_opted_in(tmp_path):
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"\x01\x02\x03")
    host = PluginHost(ROOT / "registry" / "index.json", allow_untrusted=True)
    result = host.execute("inspect_binary", file_path=sample)
    assert result["success"] is True
    assert result["output"]["size_bytes"] == 3
    assert result["output"]["modified"] is False
