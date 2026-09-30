from dataclasses import dataclass
from pathlib import Path
from app.config import MAX_FILE_BYTES, SUPPORTED_EXTENSIONS, IGNORED_DIRS

@dataclass
class SourceFile:
    file_path: str
    source: str
    language: str

LANGUAGES = {".py":"python", ".js":"javascript", ".ts":"typescript", ".java":"java", ".cpp":"cpp", ".c":"c", ".h":"c", ".hpp":"cpp", ".cs":"csharp", ".go":"go", ".rs":"rust", ".php":"php", ".rb":"ruby"}

def load_files(root, extensions=None, max_file_bytes=MAX_FILE_BYTES):
    # Users often paste Windows paths wrapped in quotes from Explorer or a
    # terminal. Remove only matching outer quotes before resolving the path.
    root_text = str(root).strip()
    if len(root_text) >= 2 and root_text[0] == root_text[-1] and root_text[0] in {'"', "'"}:
        root_text = root_text[1:-1].strip()
    root = Path(root_text).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Codebase folder does not exist or is not a directory: {root}")
    allowed = set(extensions or SUPPORTED_EXTENSIONS)
    files = []
    for path in sorted(root.rglob("*")):
        if any(part in IGNORED_DIRS for part in path.parts) or not path.is_file() or path.suffix.lower() not in allowed:
            continue
        try:
            if path.stat().st_size > max_file_bytes:
                continue
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if source.strip():
            files.append(SourceFile(path.relative_to(root).as_posix(), source, LANGUAGES.get(path.suffix.lower(), path.suffix[1:])))
    return files
