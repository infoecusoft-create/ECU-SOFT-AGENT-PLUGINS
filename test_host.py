import unittest, subprocess, sys, tempfile
from pathlib import Path
from plugin_host import PluginHost

class HostTests(unittest.TestCase):
    def test_discovery_is_metadata_only(self):
        root = Path(__file__).resolve().parents[1]
        code = "from plugin_host import PluginHost; import sys; h=PluginHost(); assert h.discover('toyota.identify_vehicle','.bin'); assert 'toyota_plugin.tool' not in sys.modules"
        subprocess.run([sys.executable, "-c", code], cwd=root, check=True)

    def test_no_modify_capability_registered(self):
        host = PluginHost()
        for action in ("toyota.set_speed", "toyota.set_rpm", "toyota.set_cutoff"):
            self.assertEqual(host.discover(action), [])

    def test_host_executes_read_only_capability(self):
        host = PluginHost()
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "unknown.bin"
            f.write_bytes(b"x" * 123)
            result = host.execute("toyota.identify_vehicle", file_path=str(f))
            self.assertTrue(result["success"])
            self.assertEqual(result["data"]["status"], "unsupported_size")

if __name__ == "__main__":
    unittest.main()
