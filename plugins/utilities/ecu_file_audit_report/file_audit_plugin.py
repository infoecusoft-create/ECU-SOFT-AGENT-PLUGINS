"""Minimal pinned ECU SOFT public loader for the file audit report tool.

This archive contains executable Python and may be extracted by recipients.
"""
import hashlib,importlib,sys,zipfile
from pathlib import Path

ARCHIVE=Path(__file__).resolve().with_name("file-audit-engine-v1.dat")
EXPECTED="ebab1fb218d392fd8ef2240c6ae7e3dfe8ade97687035e717d8ddf8156084edc"

def execute(action,params):
    if not ARCHIVE.is_file() or ARCHIVE.stat().st_size>1048576:
        return {"success":False,"error":"File-audit engine package missing or oversized"}
    if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()!=EXPECTED:
        return {"success":False,"error":"File-audit engine package SHA256 mismatch"}
    with zipfile.ZipFile(ARCHIVE) as z:
        if z.namelist()!=["audit_engine.py"] or z.testzip() is not None:
            return {"success":False,"error":"Unverified file-audit package"}
    if str(ARCHIVE) not in sys.path:sys.path.insert(0,str(ARCHIVE))
    return importlib.import_module("audit_engine").execute(action,params)
