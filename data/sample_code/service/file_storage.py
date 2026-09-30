"""Safe local upload storage helpers."""
from pathlib import Path
import uuid

UPLOAD_ROOT=Path("data/uploads")
ALLOWED_SUFFIXES={".txt", ".csv", ".json", ".png", ".jpg"}

def safe_upload_path(filename, root=UPLOAD_ROOT):
    suffix=Path(filename).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise ValueError("File type is not allowed")
    return Path(root)/(uuid.uuid4().hex+suffix)

def save_upload(filename, content, root=UPLOAD_ROOT, max_bytes=2_000_000):
    if len(content)>max_bytes:
        raise ValueError("Upload exceeds the size limit")
    target=safe_upload_path(filename,root)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(content)
    return target
