from app.ingestion.file_loader import SourceFile
from app.ingestion.chunker import chunk_file

def test_python_functions_keep_names_and_line_numbers():
    source=SourceFile("example.py","def alpha():\n    return 1\n\ndef beta():\n    return 2\n","python")
    chunks=chunk_file(source,min_lines=1)
    assert [c["symbol_name"] for c in chunks]==["alpha","beta"]
    assert chunks[0]["start_line"]==1 and chunks[1]["start_line"]==4

def test_invalid_python_falls_back_to_bounded_chunk():
    source=SourceFile("broken.py","def broken(:\n    pass\n", "python")
    assert chunk_file(source)[0]["symbol_name"]=="module"
