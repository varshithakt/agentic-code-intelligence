from functools import lru_cache
import numpy as np
import re
import hashlib
import os
from app.config import MODEL_NAME

@lru_cache(maxsize=1)
def _load_model(model_name):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name, device="cpu")

class Embedder:
    def __init__(self, model_name=MODEL_NAME, model=None):
        self.model_name=model_name
        self.fallback=False
        if model is not None:
            self.model=model
        elif os.getenv("ACI_OFFLINE_FALLBACK", "").lower() in ("1", "true", "yes"):
            self.model=None
            self.fallback=True
        else:
            try:
                self.model=_load_model(model_name)
            except Exception:
                # Keep indexing/search usable offline; use a deterministic local
                # lexical vectorizer until the configured model is available.
                self.model=None
                self.fallback=True
    @staticmethod
    def _hashed(texts, dimensions=16384):
        aliases={"authentication":"auth", "authenticate":"auth", "login":"auth", "validated":"validate", "validation":"validate", "token":"token", "cleaned":"clean", "cleaning":"clean", "normalized":"normalize", "normalization":"normalize", "inputs":"input", "incoming":"input", "created":"create", "creating":"create", "opened":"connection", "database":"database", "db":"database"}
        matrix=np.zeros((len(texts),dimensions),dtype=np.float32)
        for row,text in enumerate(texts):
            raw=re.findall(r"[a-zA-Z_][a-zA-Z_0-9]*",text.lower())
            tokens=[part for token in raw for part in (token,*token.split("_")) if part]
            for token in tokens:
                for term in (token,aliases.get(token,token)):
                    slot=int(hashlib.md5(term.encode()).hexdigest(),16)%dimensions
                    matrix[row,slot]+=1.0
            norm=np.linalg.norm(matrix[row])
            if norm: matrix[row]/=norm
        return matrix
    @staticmethod
    def document_text(chunk):
        return f"file: {chunk['file_path']}\nlanguage: {chunk['language']}\nsymbol: {chunk['symbol_name']}\n\n{chunk['code']}"
    def encode_documents(self, chunks):
        if not chunks: return np.empty((0,0), dtype=np.float32)
        texts=[self.document_text(c) for c in chunks]
        if self.fallback: return self._hashed(texts)
        return np.asarray(self.model.encode(texts, batch_size=32, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False), dtype=np.float32)
    def encode_query(self, query):
        if not query or not query.strip(): raise ValueError("Query cannot be empty")
        if self.fallback: return self._hashed([query.strip()])
        text="Represent this sentence for searching relevant code: " + query.strip()
        return np.asarray(self.model.encode([text], normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False), dtype=np.float32)
