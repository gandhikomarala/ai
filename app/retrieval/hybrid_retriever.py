from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from app.ai.embeddings.base import MockEmbeddingProvider

@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    title: str
    content: str
    score: float
    retrieval_source: str # dense, sparse, hybrid
    metadata: Dict[str, Any]

class HybridRetriever:
    def __init__(self, embedding_provider=None, rrf_k: int = 60):
        self.embedder = embedding_provider or MockEmbeddingProvider()
        self.rrf_k = rrf_k
        # In-memory document store for local execution & tests
        self._index = []

    def index_chunk(self, chunk: RetrievedChunk):
        self._index.append(chunk)

    async def retrieve_dense(self, query: str, top_k: int = 20) -> List[RetrievedChunk]:
        # Vector similarity scoring
        query_vec = await self.embedder.embed_query(query)
        results = []
        for c in self._index:
            chunk_vec = await self.embedder.embed_query(c.content)
            sim = float(np.dot(query_vec, chunk_vec))
            results.append(RetrievedChunk(
                chunk_id=c.chunk_id,
                document_id=c.document_id,
                title=c.title,
                content=c.content,
                score=sim,
                retrieval_source="dense",
                metadata=c.metadata
            ))
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    async def retrieve_sparse(self, query: str, top_k: int = 20) -> List[RetrievedChunk]:
        # BM25 / Keyword matching
        terms = set(query.lower().split())
        results = []
        for c in self._index:
            content_lower = c.content.lower()
            matches = sum(1 for t in terms if t in content_lower)
            if matches > 0:
                score = matches / max(1, len(terms))
                results.append(RetrievedChunk(
                    chunk_id=c.chunk_id,
                    document_id=c.document_id,
                    title=c.title,
                    content=c.content,
                    score=score,
                    retrieval_source="sparse",
                    metadata=c.metadata
                ))
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    async def retrieve_hybrid(self, query: str, top_k: int = 10) -> List[RetrievedChunk]:
        dense_results = await self.retrieve_dense(query, top_k=top_k * 2)
        sparse_results = await self.retrieve_sparse(query, top_k=top_k * 2)

        # Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, RetrievedChunk] = {}

        for rank, item in enumerate(dense_results):
            rrf_scores[item.chunk_id] = rrf_scores.get(item.chunk_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))
            chunk_map[item.chunk_id] = item

        for rank, item in enumerate(sparse_results):
            rrf_scores[item.chunk_id] = rrf_scores.get(item.chunk_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))
            chunk_map[item.chunk_id] = item

        fused = []
        for cid, score in rrf_scores.items():
            item = chunk_map[cid]
            fused.append(RetrievedChunk(
                chunk_id=item.chunk_id,
                document_id=item.document_id,
                title=item.title,
                content=item.content,
                score=score,
                retrieval_source="hybrid_rrf",
                metadata=item.metadata
            ))

        fused.sort(key=lambda x: x.score, reverse=True)
        return fused[:top_k]

import numpy as np
hybrid_retriever = HybridRetriever()
