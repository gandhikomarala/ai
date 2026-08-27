from typing import List
from app.retrieval.hybrid_retriever import RetrievedChunk

class RerankerService:
    def __init__(self, provider: str = "flashrank"):
        self.provider = provider

    def rerank(self, query: str, chunks: List[RetrievedChunk], top_n: int = 10) -> List[RetrievedChunk]:
        if not chunks:
            return []
        query_words = set(query.lower().split())
        reranked = []
        for c in chunks:
            content_words = set(c.content.lower().split())
            overlap = len(query_words.intersection(content_words))
            cross_score = c.score * 0.5 + (overlap / max(1, len(query_words))) * 0.5
            reranked.append(RetrievedChunk(
                chunk_id=c.chunk_id,
                document_id=c.document_id,
                title=c.title,
                content=c.content,
                score=cross_score,
                retrieval_source=f"reranked_{self.provider}",
                metadata=c.metadata
            ))
        reranked.sort(key=lambda x: x.score, reverse=True)
        return reranked[:top_n]

reranker_service = RerankerService()
