"""ECU SOFT public, hash-checked archive loader; original source is stored privately."""
import hashlib,importlib,sys,zipfile
from pathlib import Path
PACKAGE=Path(__file__).resolve().with_name("file-hash-engine-v0.1.0.dat")
EXPECTED="9fa09fd500f440031154b0ae18739beb59358d43d531fe2a195c28126cebc8d3"
def execute(action,params):
    if not PACKAGE.is_file() or PACKAGE.stat().st_size>1024*1024:
        return {"success":False,"error":"Executable archive missing or oversized"}
    if hashlib.sha256(PACKAGE.read_bytes()).hexdigest()!=EXPECTED:
        return {"success":False,"error":"Executable archive fingerprint mismatch"}
    with zipfile.ZipFile(PACKAGE) as z:
        if z.namelist()!=["hash_engine.py"] or z.testzip() is not None:
            return {"success":False,"error":"Executable archive entry not verified"}
    if str(PACKAGE) not in sys.path:sys.path.insert(0,str(PACKAGE))
    return importlib.import_module("hash_engine").execute(action,params)
