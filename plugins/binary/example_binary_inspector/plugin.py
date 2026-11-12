"""Read-only example plugin."""
import hashlib
from pathlib import Path


class BinaryInspector:
    def execute(self, operation, inputs, context=None):
        if operation != "inspect_binary":
            raise ValueError(f"Unsupported operation: {operation}")
        file_path = Path(inputs["file_path"])
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        digest = hashlib.sha256()
        size = 0
        with file_path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(chunk)
                digest.update(chunk)
        return {
            "file_name": file_path.name,
            "size_bytes": size,
            "sha256": digest.hexdigest(),
            "modified": False
        }


def create_plugin():
    return BinaryInspector()
