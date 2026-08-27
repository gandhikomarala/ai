# ADR-002: Reciprocal Rank Fusion (RRF) for Dense + Sparse Hybrid Search

## Status
Accepted

## Context
Dense vector search excels at conceptual similarity but can miss exact keyword lookups (e.g. error codes `INC-2841`, function names `validate_token`, UUIDs).

## Decision
Adopt Reciprocal Rank Fusion (RRF) with $k=60$ combining `pgvector` dense cosine retrieval and PostgreSQL `tsvector` BM25 keyword search, followed by a Cross-Encoder Reranker.

## Tradeoffs
- Higher retrieval quality across both keyword and semantic queries.
- Slight additional compute during multi-index candidate gathering.
