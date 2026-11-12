import hashlib
from pathlib import Path
def execute(action, params):
    p = Path(params["file_path"])
    data = p.read_bytes()
    return {"success": True, "file": p.name, "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "read_only": True}
