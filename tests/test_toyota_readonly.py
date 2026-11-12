import unittest, tempfile, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "plugins" / "toyota" / "toyo_limiter"))
from toyota_plugin.tool import _load_profiles, identify_vehicle, execute

class ToyotaReadOnlyTests(unittest.TestCase):
    def test_profiles_preserve_duplicate_variant(self):
        items = [p for p in _load_profiles() if p["source_name"] == "hilux_GIN1_3_1"]
        self.assertEqual(len(items), 2)
        self.assertTrue(all(p.get("_source_conflict") for p in items))

    def test_unknown_size_is_not_guessed(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "unknown.bin"; f.write_bytes(b"x" * 123)
            self.assertEqual(identify_vehicle(f)["status"], "unsupported_size")

    def test_mutation_actions_not_exposed(self):
        for a in ("set_speed", "set_rpm", "set_cutoff", "modify_bin"):
            r = execute(a, {"file_path": "does-not-matter.bin"})
            self.assertFalse(r["success"])

if __name__ == "__main__":
    unittest.main()
