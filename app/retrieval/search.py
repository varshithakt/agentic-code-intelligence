import time
from app.retrieval.embedder import Embedder
from app.retrieval.index import IndexManager
from app.config import INDEX_DIR

class CodeSearch:
    def __init__(self, manager=None, embedder=None): self.manager=manager or IndexManager(INDEX_DIR); self.embedder=embedder or Embedder()
    def search(self, query, top_k=5, literal_filter=None):
        start=time.perf_counter(); vector=self.embedder.encode_query(query)
        if literal_filter:
            candidates=self.manager.search(vector,self.manager.index.ntotal)
            needle=literal_filter.casefold()
            results=[r for r in candidates if needle in r["code"].casefold()][:top_k]
        else:
            results=self.manager.search(vector,top_k)
        return results, (time.perf_counter()-start)*1000
