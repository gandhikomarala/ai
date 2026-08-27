from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass, field
from app.core.constants import ChunkingStrategy

@dataclass
class RawChunk:
    content: str
    chunk_index: int
    token_count: int
    strategy: ChunkingStrategy
    page_number: int = 1
    section_title: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_chunk_index: int = -1

class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[RawChunk]:
        pass

    def estimate_tokens(self, text: str) -> int:
        return max(1, len(text.split()) * 4 // 3)
