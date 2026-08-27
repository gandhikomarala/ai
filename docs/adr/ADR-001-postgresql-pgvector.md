# ADR-001: PostgreSQL with pgvector as Core Unified Storage

## Status
Accepted

## Context
AegisAI requires relational metadata (tenants, RBAC, documents, commits, incidents), full-text keyword search (BM25 approximation), and vector embeddings for dense semantic retrieval.

## Decision
Adopt PostgreSQL 16 with `pgvector` and `pg_trgm` extensions as the primary unified database rather than running separate dedicated vector databases (e.g. Pinecone/Qdrant) during baseline deployment.

## Consequences
- **Pros**: ACID transactions across metadata and embeddings, zero sync drift between documents and vectors, unified Row-Level Security.
- **Cons**: Requires tuning HNSW index parameters for multi-million vector datasets.
