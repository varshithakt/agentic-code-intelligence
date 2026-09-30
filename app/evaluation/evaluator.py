import time
from app.evaluation.metrics import mean_ndcg, mrr
from app.retrieval.query_processor import preprocess_query

class LocalEvaluator:
    def __init__(self, searcher): self.searcher=searcher

    def evaluate(self, dataset, top_k=10, candidate_pool=30, rerank=False):
        report={}
        for strategy in ("semantic", "bm25", "hybrid", "hybrid_rerank"):
            rows=[]; started=time.perf_counter()
            for item in dataset:
                relevant=item["relevant_chunk_ids"]
                if strategy=="hybrid": results,_,_=self.searcher.search(item["query"],top_k,candidate_pool=candidate_pool,rerank=False)
                elif strategy=="hybrid_rerank": results,_,_=self.searcher.search(item["query"],top_k,candidate_pool=candidate_pool,rerank=True)
                else:
                    processed=preprocess_query(item["query"])["normalized_query"]
                    if strategy=="semantic": raw=self.searcher.manager.search(self.searcher.embedder.encode_query(processed),top_k)
                    else: raw=self.searcher.manager.search_bm25(processed,top_k)
                    results=raw
                rows.append(([result["chunk_id"] for result in results], relevant))
            report[strategy]={"ndcg@10":round(mean_ndcg(rows,10),6),"mrr":round(mrr(rows),6),"queries":len(rows),"latency_ms":round((time.perf_counter()-started)*1000,2)}
        return {"dataset":"Local Development","results":report}
