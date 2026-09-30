from app.retrieval.embedder import Embedder
from app.retrieval.index import IndexManager
from app.ingestion.file_loader import load_files
from app.ingestion.chunker import chunk_files
from app.config import INDEX_DIR

def build_code_index(path, directory=INDEX_DIR, embedder=None):
    files=load_files(path)
    if not files: raise ValueError("No supported, readable source files found in this folder")
    chunks=chunk_files(files)
    emb=embedder or Embedder()
    manager=IndexManager(directory); manager.build(chunks,emb.encode_documents(chunks)); manager.save()
    return {"files_indexed":len(files),"chunks_indexed":len(chunks),"index_status":"Ready","embedding_mode":"local lexical fallback" if emb.fallback else emb.model_name}
