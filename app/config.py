from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = Path(os.getenv("ACI_INDEX_DIR", ROOT / "data" / "index"))
MODEL_NAME = os.getenv("ACI_MODEL", "BAAI/bge-small-en-v1.5")
MAX_FILE_BYTES = int(os.getenv("ACI_MAX_FILE_BYTES", str(1_000_000)))
MIN_CHUNK_LINES = int(os.getenv("ACI_MIN_CHUNK_LINES", "3"))
MAX_CHUNK_LINES = int(os.getenv("ACI_MAX_CHUNK_LINES", "80"))
CHUNK_OVERLAP = int(os.getenv("ACI_CHUNK_OVERLAP", "8"))
RERANK_ENABLED = os.getenv("ACI_RERANK_ENABLED", "false").lower() in {"1", "true", "yes"}
SUPPORTED_EXTENSIONS = {".py", ".java", ".js", ".ts", ".cpp", ".c", ".h", ".hpp", ".cs", ".go", ".rs", ".php", ".rb"}
IGNORED_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build", "target"}
