from pathlib import Path
from app.ingestion.file_loader import load_files
from app.ingestion.chunker import chunk_files

ROOT=Path(__file__).resolve().parents[1]

def test_sample_queries_have_relevant_chunks_in_top_k():
    chunks=chunk_files(load_files(ROOT/"data"/"sample_code"))
    assert len(chunks)>=30
    cases=[("authentication token validated",("auth.py","validate_token")),("database connection created",("database.py","create_connection")),("normalize email input",("input_cleaning.py","normalize_email"))]
    for query,(filename,symbol) in cases:
        terms=set(query.lower().split())
        ranked=sorted(chunks,key=lambda c:sum(t in (c["symbol_name"]+" "+c["code"]).lower() for t in terms),reverse=True)
        assert any(filename in c["file_path"] and symbol==c["symbol_name"] for c in ranked[:20])

def test_loader_reads_sample_sources():
    files=load_files(ROOT/"data"/"sample_code")
    assert len(files)>=10
    assert any(f.file_path=="service/auth.py" for f in files)
