from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.models.schemas import BuildRequest, SearchRequest
from app.retrieval.index import IndexManager
from app.retrieval.search import CodeSearch
from app.utils.helpers import build_code_index
from app.config import INDEX_DIR

app=FastAPI(title="Agentic Code Intelligence")
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
        results,latency=searcher.search(req.query,req.top_k,req.literal_filter)
        return {"results":results,"latency_ms":round(latency,2)}
    except ValueError as exc: raise HTTPException(400,str(exc)) from exc
    except Exception as exc: raise HTTPException(500,"Search failed. Check the local model and index files.") from exc
