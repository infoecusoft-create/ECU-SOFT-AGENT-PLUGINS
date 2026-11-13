"""Public IVECO archive verification adapter for unchanged dynamic ECU SOFT MCPB.
Not an OS sandbox. Engineering source is shipped as pinned zip archive data.
"""
import hashlib
import importlib
import sys
import zipfile
from pathlib import Path

_ARCHIVE=Path(__file__).resolve().with_name("iveco-engine-v0.1.0.dat")
_SHA256="fcaed88aa20c4114e0849a3f9ade4e2bfc8998b6791c0ba06e81d54ad814a75f"

def _engine():
    if not _ARCHIVE.is_file() or _ARCHIVE.stat().st_size>3*1024*1024:
        raise RuntimeError("IVECO engine archive missing or oversized")
    if hashlib.sha256(_ARCHIVE.read_bytes()).hexdigest()!=_SHA256:
        raise RuntimeError("IVECO engine archive SHA256 mismatch")
    with zipfile.ZipFile(_ARCHIVE) as z:
        names=z.namelist()
        if not names or len(names)>100 or z.testzip() is not None:
            raise RuntimeError("Invalid IVECO engine archive")
        for n in names:
            if (not n.endswith(".py") or n.startswith("/")
                or any(s in ("",".","..") for s in n.split("/"))
                or not (n=="iveco_runtime_entry.py" or n.startswith("vcm_limiter/"))):
                raise RuntimeError("Unsafe IVECO engine archive member")
    if str(_ARCHIVE) not in sys.path:
        sys.path.insert(0,str(_ARCHIVE))
    return importlib.import_module("iveco_runtime_entry")

def execute(action,params):
    return _engine().execute(action,params)
