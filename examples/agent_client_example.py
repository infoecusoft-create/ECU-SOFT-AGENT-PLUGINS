"""Minimal local client example."""
from pathlib import Path
from plugin_host import PluginHost

ROOT = Path(__file__).resolve().parents[1]
host = PluginHost(ROOT / "registry" / "index.json", allow_untrusted=True)

print(host.discover(operation="inspect_binary", extension=".bin"))
# Example:
# result = host.execute("inspect_binary", file_path="sample.bin")
# print(result)
