from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.models.schemas import BuildRequest, SearchRequest
from app.retrieval.index import IndexManager
from app.retrieval.search import CodeSearch
from app.utils.helpers import build_code_index
from app.config import INDEX_DIR, MODEL_NAME
from app.evaluation.datasets import load_local_dataset
from app.evaluation.evaluator import LocalEvaluator

app=FastAPI(title="CodeSeek")
STATIC=Path(__file__).resolve().parents[1]/"static"
app.mount("/static",StaticFiles(directory=STATIC),name="static")
manager=IndexManager(INDEX_DIR); searcher=None; index_status={"index_status":"Not built","files_indexed":0,"chunks_indexed":0}
@app.get("/")
def home(): return FileResponse(STATIC/"index.html")
@app.get("/api/status")
def status(): return index_status
@app.post("/api/build")
def build(req:BuildRequest):
    global manager,searcher,index_status
    try:
        index_status=build_code_index(req.path)
        manager=IndexManager(INDEX_DIR).load(); searcher=CodeSearch(manager=manager)
        return index_status
    except (ValueError,RuntimeError,FileNotFoundError) as exc: raise HTTPException(400,str(exc)) from exc
    except Exception as exc: raise HTTPException(500,"Index build failed. Check the model and dependency setup.") from exc
@app.post("/api/search")
def search(req:SearchRequest):
    global searcher
    if searcher is None:
        try: searcher=CodeSearch(manager=IndexManager(INDEX_DIR).load())
        except Exception: raise HTTPException(409,"Build an index before searching")
    try:
        results,latency,details=searcher.search(req.query,req.top_k,req.literal_filter,req.alpha,req.rerank,req.candidate_k or req.candidate_pool,req.version_id)
        return {"results":results,**details}
    except ValueError as exc: raise HTTPException(400,str(exc)) from exc
    except Exception as exc: raise HTTPException(500,"Search failed. Check the local model and index files.") from exc

@app.post("/search")
def search_alias(req:SearchRequest):
    return search(req)

@app.get("/stats")
def stats():
    global manager
    if manager.index is None:
        try: manager.load()
        except Exception: pass
    loaded = manager.index is not None
    return {"files": len({item.get("file_path") for item in manager.metadata}), "chunks": len(manager.metadata), "embedding_model": getattr(getattr(searcher, "embedder", None), "model_name", MODEL_NAME), "embedding_dimension": manager.index.d if loaded else None, "faiss_ready": loaded, "bm25_ready": loaded and bool(manager.bm25.tokens), "reranker_ready": True, "index_creation_time": manager.created_at, "supported_languages": sorted({item.get("language") for item in manager.metadata})}

@app.get("/evaluation/local")
def local_evaluation():
    global searcher
    if searcher is None:
        try: searcher=CodeSearch(manager=IndexManager(INDEX_DIR).load())
        except Exception: raise HTTPException(409,"Build an index before evaluating")
    try: return LocalEvaluator(searcher).evaluate(load_local_dataset(),10)
    except Exception as exc: raise HTTPException(500,"Local evaluation failed") from exc
