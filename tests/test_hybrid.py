from pathlib import Path
from app.ingestion.file_loader import load_files
from app.ingestion.chunker import chunk_files
from app.retrieval.bm25_index import BM25Index, tokenize
from app.retrieval.query_processor import preprocess_query

ROOT=Path(__file__).resolve().parents[1]

def test_query_processor_preserves_identifiers():
    result=preprocess_query("Where is JWT token validation performed before API access?")
    assert "JWT" in result["technical_terms"]
    assert "API" in result["technical_terms"]
    assert "validation" in result["keywords"]

def test_bm25_indexes_identifiers_and_returns_matching_chunk():
    chunks=chunk_files(load_files(ROOT/"data"/"sample_code"))
    index=BM25Index(ROOT/"data"/"index-test").build(chunks)
    matches=index.search("create_connection database",5)
    assert matches
    assert chunks[matches[0][1]]["symbol_name"]=="create_connection"
    assert "validate" in tokenize("validateJWTToken")
