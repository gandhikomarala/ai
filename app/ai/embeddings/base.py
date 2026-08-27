import hashlib
import numpy as np
from typing import List
from abc import ABC, abstractmethod

class BaseEmbeddingProvider(ABC):
    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        pass

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        pass

class MockEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension

    async def embed_query(self, text: str) -> List[float]:
        # Deterministic pseudo-embedding based on hash
        seed = int(hashlib.md5(text.encode("utf-8")).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed)
        vec = rng.randn(self.dimension).astype(float)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [await self.embed_query(t) for t in texts]
