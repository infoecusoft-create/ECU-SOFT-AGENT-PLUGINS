"""Versioned immutable ECU SOFT byte entropy engine loader."""
from pathlib import Path
import hashlib,zipfile,sys,importlib
ARCHIVE=Path(__file__).resolve().with_name("byte-entropy-engine-v1.dat")
EXPECTED="51943b02a91315e448e9729b566c5f85a0f8a11ae5f9aee0934ef56d622d1818"
def execute(action,params):
    if not ARCHIVE.is_file() or ARCHIVE.stat().st_size>1024*1024:
        return {"success":False,"error":"Engine archive missing or too large"}
    if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()!=EXPECTED:
        return {"success":False,"error":"Engine archive checksum mismatch"}
    with zipfile.ZipFile(ARCHIVE) as z:
        if z.namelist()!=["entropy_engine.py"] or z.testzip() is not None:
            return {"success":False,"error":"Invalid engine package"}
    if str(ARCHIVE) not in sys.path:sys.path.insert(0,str(ARCHIVE))
    return importlib.import_module("entropy_engine").execute(action,params)
