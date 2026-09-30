"""Deterministic query normalization that preserves code identifiers."""
import re

STOP_WORDS = {"a", "an", "the", "is", "are", "where", "how", "what", "which", "before", "after", "and", "or", "to", "in", "of", "for", "does", "do", "this", "that"}

def _tokens(text):
    raw = re.findall(r"[A-Za-z_][A-Za-z0-9_.$/-]*", text)
    result = []
    for value in raw:
        result.append(value)
        parts = re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", value)
        result.extend(parts)
    return result

def preprocess_query(query):
    original = (query or "").strip()
    terms = [token for token in _tokens(original) if token.casefold() not in STOP_WORDS and len(token) > 1]
    unique = list(dict.fromkeys(terms))
    normalized = " ".join(unique)
    technical = [token for token in unique if "_" in token or any(char.isupper() for char in token) or token.casefold() in {"api", "jwt", "json", "http", "sql", "faiss", "bm25", "token", "database"}]
    return {"original_query": original, "normalized_query": normalized, "keywords": unique, "technical_terms": list(dict.fromkeys(technical))}
