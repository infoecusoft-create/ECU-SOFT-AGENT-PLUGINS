import json
import tempfile
import unittest
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from toyota_plugin.tool import identify_vehicle, inspect_bin, execute, _load_profiles

class ToyotaReadOnlyTests(unittest.TestCase):
    def test_profiles_loaded_and_duplicate_preserved(self):
        profiles=_load_profiles()
        self.assertGreaterEqual(len(profiles), 20)
        dup=[p for p in profiles if p.get("source_name")=="hilux_GIN1_3_1"]
        self.assertEqual(len(dup),2)
        self.assertTrue(all(p.get("_source_conflict") for p in dup))

    def test_unsupported_size(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"unknown.bin"; p.write_bytes(b"x"*123)
            r=identify_vehicle(p)
            self.assertEqual(r["status"],"unsupported_size")

    def test_extension_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.dat"; p.write_bytes(b"x")
            r=execute("inspect_bin",{"file_path":str(p)})
            self.assertFalse(r["success"])

    def test_synthetic_read_only_inspection(self):
        import hashlib
        from toyota_plugin.tool import _pattern
        profile=next(p for p in _load_profiles() if p["source_name"]=="forchenar_GIN1")
        blob=bytearray(profile["EXPECTED_SIZE"])
        start=_pattern(profile["PATTERN_START"])
        blob[100:100+len(start)]=start
        speed_at=100+len(start)
        blob[speed_at:speed_at+profile["SPEED_LENGTH"]]=b"\x2a"
        rstart=_pattern(profile["RPM_PATTERN_START"])
        rend=_pattern(profile["RPM_PATTERN_END"])
        blob[1000:1000+len(rstart)]=rstart
        blob[1040:1040+len(rend)]=rend
        blob[1020:1022]=(2500).to_bytes(2,"little")
        cut=_pattern(profile["CUT_PATTERN"])
        blob[2000:2000+len(cut)]=cut
        for i in range(6): blob[2000+len(cut)+i*2:2002+len(cut)+i*2]=(100+i).to_bytes(2,"little")
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"synthetic.bin"; p.write_bytes(blob)
            before=hashlib.sha256(p.read_bytes()).hexdigest()
            report=inspect_bin(p)
            after=hashlib.sha256(p.read_bytes()).hexdigest()
            self.assertTrue(report["success"],report)
            self.assertEqual(report["analysis"]["source_name"],"forchenar_GIN1")
            self.assertEqual(before,after)

    def test_no_mutation_api(self):
        import toyota_plugin.tool as tool
        self.assertFalse(hasattr(tool,"modify_bin"))
        self.assertFalse(hasattr(tool,"set_speed"))
        self.assertFalse(hasattr(tool,"set_rpm"))

if __name__ == "__main__": unittest.main()
