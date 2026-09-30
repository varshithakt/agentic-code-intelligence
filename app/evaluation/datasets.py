import json
from pathlib import Path

def load_local_dataset(path=None):
    location=Path(path or Path(__file__).resolve().parents[2]/"data"/"evaluation"/"sample_queries.json")
    return json.loads(location.read_text(encoding="utf-8"))
