import logging
import time
from app.config import INDEX_DIR, RERANK_ENABLED
from app.retrieval.base import BaseRetriever
from app.retrieval.embedder import Embedder
from app.retrieval.index import IndexManager
from app.retrieval.query_processor import preprocess_query
from app.retrieval.bm25_index import tokenize

logger = logging.getLogger(__name__)

def _normalize(scores):
    if not scores: return {}
    values = list(scores.values()); low, high = min(values), max(values)
    if high == low: return {key: 1.0 if high > 0 else 0.0 for key in scores}
    return {key: (value - low) / (high - low) for key, value in scores.items()}

class CodeSearch(BaseRetriever):
    def __init__(self, manager=None, embedder=None):
        self.manager = manager or IndexManager(INDEX_DIR); self.embedder = embedder or Embedder()

    def search(self, query, top_k=5, literal_filter=None, alpha=0.7, rerank=None, candidate_pool=30):
        started = time.perf_counter(); processed = preprocess_query(query); alpha = min(1.0, max(0.0, float(alpha)))
        rerank_enabled = RERANK_ENABLED if rerank is None else bool(rerank)
        semantic_started = time.perf_counter(); semantic = self.manager.search(self.embedder.encode_query(processed["normalized_query"]), max(candidate_pool, top_k)); semantic_time = (time.perf_counter() - semantic_started) * 1000
        keyword_started = time.perf_counter(); keyword = self.manager.search_bm25(processed["normalized_query"], max(candidate_pool, top_k)); keyword_time = (time.perf_counter() - keyword_started) * 1000
        semantic_scores = {item["chunk_id"]: item["score"] for item in semantic}; keyword_scores = {item["chunk_id"]: item["score"] for item in keyword}
        semantic_norm, keyword_norm = _normalize(semantic_scores), _normalize(keyword_scores)
        merged = {item["chunk_id"]: item for item in semantic + keyword}; query_terms = set(tokenize(processed["normalized_query"])); candidates = []
        for chunk_id, item in merged.items():
            if literal_filter and literal_filter.casefold() not in item["code"].casefold(): continue
            semantic_score, keyword_score = semantic_norm.get(chunk_id, 0.0), keyword_norm.get(chunk_id, 0.0)
            identifier_match = 1.0 if any(term in item["symbol_name"].casefold() or term in item["file_path"].casefold() for term in query_terms) else 0.0
            hybrid = alpha * semantic_score + (1 - alpha) * keyword_score + 0.05 * identifier_match
            candidates.append({**item, "semantic_score": semantic_score, "bm25_score": keyword_score, "hybrid_score": hybrid, "identifier_match": identifier_match, "rerank_score": None})
        candidates.sort(key=lambda item: item["hybrid_score"], reverse=True); rerank_time = 0.0
        if rerank_enabled and candidates:
            rerank_started = time.perf_counter()
            for item in candidates:
                item["rerank_score"] = len(query_terms & set(tokenize(item["code"]))) / max(len(query_terms), 1)
            candidates.sort(key=lambda item: 0.65 * item["hybrid_score"] + 0.35 * item["rerank_score"], reverse=True); rerank_time = (time.perf_counter() - rerank_started) * 1000
        results = []
        for rank, item in enumerate(candidates[:top_k], 1):
            item["rank"] = rank; item["score"] = item["hybrid_score"]; results.append(item)
        total = (time.perf_counter() - started) * 1000
        details = {"query": query, "processed_query": processed, "search_time_ms": round(total, 2), "retrieval_mode": "hybrid", "semantic_candidates": len(semantic), "keyword_candidates": len(keyword), "merged_candidates": len(merged), "reranking_enabled": rerank_enabled, "timings_ms": {"semantic": round(semantic_time, 2), "bm25": round(keyword_time, 2), "rerank": round(rerank_time, 2), "total": round(total, 2)}}
        logger.info("hybrid_search semantic=%d keyword=%d merged=%d rerank=%s latency_ms=%.2f", len(semantic), len(keyword), len(merged), rerank_enabled, total)
        return results, total, details
