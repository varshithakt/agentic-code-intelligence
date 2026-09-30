# CodeSeek Presentation Outline

## Slide 1 — Title

CodeSeek — Intelligent Code Retrieval

Natural-language search over real source code.

## Slide 2 — Problem

Large codebases hide implementation details behind unfamiliar files, symbols, and terminology. Exact search misses concepts; semantic search can miss identifiers.

## Slide 3 — Solution

CodeSeek combines FAISS semantic retrieval, BM25 keyword retrieval, normalized hybrid scoring, and optional reranking.

## Slide 4 — System architecture

Source folder → loader → code chunks → embeddings and BM25 → candidate fusion → ranked snippets.

## Slide 5 — Product demo

Show indexing, authentication search, database search, input normalization search, score breakdowns, and copy-to-clipboard.

## Slide 6 — Evaluation

Show the local Evaluation Lab and clearly label its NDCG@10 and MRR values as local development measurements.

## Slide 7 — Reproducibility

Show Python setup, Docker Compose, CLI commands, tests, and the tagged Git commit.

## Slide 8 — Roadmap

Official CoIR/MTEB measurement, stronger cross-encoder reranking, version-aware retrieval, and advanced ranking research.
