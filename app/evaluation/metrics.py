import math

def reciprocal_rank(results, relevant):
    relevant=set(relevant)
    for rank, chunk_id in enumerate(results, 1):
        if chunk_id in relevant: return 1.0 / rank
    return 0.0

def ndcg_at_k(results, relevant, k=10):
    relevant=set(relevant)
    gains=[1.0 if chunk_id in relevant else 0.0 for chunk_id in results[:k]]
    dcg=sum(gain / math.log2(rank + 2) for rank, gain in enumerate(gains))
    ideal=min(len(relevant), k)
    idcg=sum(1.0 / math.log2(rank + 2) for rank in range(ideal))
    return dcg / idcg if idcg else 0.0

def mrr(all_results):
    return sum(reciprocal_rank(results, relevant) for results, relevant in all_results) / max(len(all_results), 1)

def mean_ndcg(all_results, k=10):
    return sum(ndcg_at_k(results, relevant, k) for results, relevant in all_results) / max(len(all_results), 1)
