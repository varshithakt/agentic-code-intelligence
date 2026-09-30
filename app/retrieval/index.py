import json
from pathlib import Path
import numpy as np

class IndexManager:
    def __init__(self, directory):
        self.directory=Path(directory); self.index=None; self.metadata=[]
    def build(self, chunks, embeddings):
        if not chunks: raise ValueError("No code chunks were found to index")
        try: import faiss
        except ImportError as exc: raise RuntimeError("FAISS is required. Install dependencies with pip install -r requirements.txt") from exc
        vectors=np.ascontiguousarray(embeddings,dtype=np.float32)
        if vectors.ndim!=2 or len(vectors)!=len(chunks): raise ValueError("Embedding count does not match chunk count")
        faiss.normalize_L2(vectors)
        self.index=faiss.IndexFlatIP(vectors.shape[1]); self.index.add(vectors); self.metadata=chunks
    def save(self):
        if self.index is None: raise ValueError("Index has not been built")
        import faiss
        self.directory.mkdir(parents=True,exist_ok=True)
        faiss.write_index(self.index,str(self.directory/"index.faiss"))
        (self.directory/"metadata.json").write_text(json.dumps(self.metadata,ensure_ascii=False,indent=2),encoding="utf-8")
    def load(self):
        import faiss
        ip=self.directory/"index.faiss"; mp=self.directory/"metadata.json"
        if not ip.exists() or not mp.exists(): raise FileNotFoundError("Index is not built yet")
        self.index=faiss.read_index(str(ip)); self.metadata=json.loads(mp.read_text(encoding="utf-8"))
        if self.index.ntotal!=len(self.metadata): raise ValueError("Index and metadata are inconsistent")
        return self
    def search(self, query_embedding, top_k=5):
        if self.index is None: raise RuntimeError("Index is not loaded")
        k=min(max(int(top_k),1),self.index.ntotal)
        scores,positions=self.index.search(np.ascontiguousarray(query_embedding,dtype=np.float32),k)
        return [{**self.metadata[int(i)],"score":float(s)} for s,i in zip(scores[0],positions[0]) if i>=0]
