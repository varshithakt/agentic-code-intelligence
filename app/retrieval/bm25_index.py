"""Local BM25 keyword index over code chunks."""
import json
import math
import re
from pathlib import Path

def tokenize(text):
    raw = re.findall(r"[A-Za-z_][A-Za-z0-9_.$/-]*", text)
    tokens = []
    for value in raw:
        tokens.append(value.casefold())
        tokens.extend(part.casefold() for part in re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", value))
    return tokens

class BM25Index:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.documents = []
        self.tokens = []
        self.idf = {}
        self.avgdl = 0.0
        self.k1, self.b = 1.5, 0.75

    @staticmethod
    def document_text(chunk):
        return " ".join(str(chunk.get(key, "")) for key in ("file_path", "file_name", "language", "symbol_name", "symbol_type", "code"))

    def build(self, chunks):
        self.documents = [self.document_text(chunk) for chunk in chunks]
        self.tokens = [tokenize(doc) for doc in self.documents]
        self.avgdl = sum(map(len, self.tokens)) / max(len(self.tokens), 1)
        frequencies = {}
        for terms in self.tokens:
            for term in set(terms): frequencies[term] = frequencies.get(term, 0) + 1
        count = len(self.tokens)
        self.idf = {term: math.log(1 + (count - freq + 0.5) / (freq + 0.5)) for term, freq in frequencies.items()}
        return self

    def search(self, query, top_k=30):
        query_terms = tokenize(query)
        scores = []
        for position, terms in enumerate(self.tokens):
            counts = {term: terms.count(term) for term in set(query_terms)}
            score = 0.0
            for term, frequency in counts.items():
                if not frequency: continue
                score += self.idf.get(term, 0.0) * frequency * (self.k1 + 1) / (frequency + self.k1 * (1 - self.b + self.b * len(terms) / max(self.avgdl, 1)))
            scores.append((score, position))
        return sorted(scores, reverse=True)[:max(1, int(top_k))]

    def save(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        (self.directory / "bm25.json").write_text(json.dumps({"documents": self.documents, "tokens": self.tokens, "idf": self.idf, "avgdl": self.avgdl}), encoding="utf-8")

    def load(self):
        payload = json.loads((self.directory / "bm25.json").read_text(encoding="utf-8"))
        self.documents, self.tokens, self.idf, self.avgdl = payload["documents"], payload["tokens"], payload["idf"], payload["avgdl"]
        return self
