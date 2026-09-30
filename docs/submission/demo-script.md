# CodeSeek — Six-Minute Demo Script

## 0:00–0:30 — Problem

CodeSeek is an intelligent code retrieval system for large codebases. A developer can ask a natural-language question and receive the actual relevant functions, classes, and source snippets instead of a generated chatbot answer.

## 0:30–1:15 — Indexing

Enter a local source folder and select **Build Index**. CodeSeek loads supported source files, detects Python functions and classes, chunks other languages safely, generates CPU embeddings, and builds both FAISS and BM25 indexes. The dashboard reports files, chunks, and index health.

## 1:15–2:15 — Semantic and keyword retrieval

Search `Where is JWT token validation performed?`. The system preserves technical identifiers, searches semantic and keyword indexes, merges duplicate chunks, normalizes the scores, and ranks the result. The top result is `validate_token` in `service/auth.py`, with its line range and source code.

## 2:15–3:15 — Hybrid ranking

Search `Where is the database connection initialized?` and then `How is user input normalized?`. FAISS handles conceptual similarity while BM25 gives exact identifiers and filenames strong signals. The result card shows semantic, keyword, hybrid, and factual identifier-match signals.

## 3:15–4:00 — Settings and developer workflow

Open Retrieval Settings. Semantic weight, candidate pool, top K, and reranking are real API controls. Copy a result with **COPY**. Recent searches are kept locally in browser storage, and `Ctrl+Enter` submits a query.

## 4:00–5:15 — Evaluation

Open Evaluation and run the local development benchmark. CodeSeek compares semantic-only, BM25-only, hybrid, and hybrid-plus-reranker retrieval using NDCG@10 and MRR. These are measured local results from `data/evaluation/sample_queries.json`, not fabricated official benchmark scores.

## 5:15–6:00 — Architecture and close

The pipeline is query preprocessing, FAISS semantic retrieval, BM25 retrieval, candidate fusion, normalized hybrid scoring, optional reranking, and ranked source snippets. CodeSeek runs locally, exposes API timing, supports Docker, and includes an adapter prepared for the official MTEB AppsRetrieval workflow. Future work includes stronger reranking and version-aware retrieval.
