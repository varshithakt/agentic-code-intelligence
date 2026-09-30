from app.evaluation.metrics import ndcg_at_k, reciprocal_rank
from app.retrieval.search import normalize_scores

def test_metrics_known_ranking():
    assert reciprocal_rank(["a", "b"], ["b"]) == 0.5
    assert round(ndcg_at_k(["a", "b"], ["b"], 2), 6) == round(1 / 1.5849625, 6)

def test_normalization_handles_empty_constant_and_negative_scores():
    assert normalize_scores({}) == {}
    assert normalize_scores({"a": 2, "b": 2}) == {"a": 1.0, "b": 1.0}
    normalized=normalize_scores({"a": -2, "b": 0, "c": 2})
    assert normalized=={"a": 0.0, "b": 0.5, "c": 1.0}
