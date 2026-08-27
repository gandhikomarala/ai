import re
from typing import List, Dict, Any
from app.ingestion.chunkers.base import BaseChunker, RawChunk
from app.core.constants import ChunkingStrategy

class FixedSizeChunker(BaseChunker):
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[RawChunk]:
        words = text.split()
        chunks = []
        idx = 0
        i = 0
        while i < len(words):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append(RawChunk(
                content=chunk_text,
                chunk_index=idx,
                token_count=self.estimate_tokens(chunk_text),
                strategy=ChunkingStrategy.FIXED,
                metadata=metadata
            ))
            idx += 1
            i += self.chunk_size - self.overlap
            if i >= len(words) and len(chunk_words) < self.chunk_size:
                break
        return chunks

class SentenceChunker(BaseChunker):
    def __init__(self, max_tokens: int = 400):
        self.max_tokens = max_tokens

    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[RawChunk]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current = []
        current_tokens = 0
        idx = 0
        for s in sentences:
            s_tokens = self.estimate_tokens(s)
            if current_tokens + s_tokens > self.max_tokens and current:
                c_text = " ".join(current)
                chunks.append(RawChunk(
                    content=c_text,
                    chunk_index=idx,
                    token_count=current_tokens,
                    strategy=ChunkingStrategy.SENTENCE,
                    metadata=metadata
                ))
                idx += 1
                current = [s]
                current_tokens = s_tokens
            else:
                current.append(s)
                current_tokens += s_tokens
        if current:
            c_text = " ".join(current)
            chunks.append(RawChunk(
                content=c_text,
                chunk_index=idx,
                token_count=current_tokens,
                strategy=ChunkingStrategy.SENTENCE,
                metadata=metadata
            ))
        return chunks

class MarkdownChunker(BaseChunker):
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[RawChunk]:
        sections = re.split(r"(?=(?:\n|^)#{1,4}\s+)", text)
        chunks = []
        idx = 0
        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue
            title_match = re.match(r"^#{1,4}\s+(.+)", sec)
            title = title_match.group(1) if title_match else "Overview"
            chunks.append(RawChunk(
                content=sec,
                chunk_index=idx,
                token_count=self.estimate_tokens(sec),
                strategy=ChunkingStrategy.MARKDOWN,
                section_title=title,
                metadata={**metadata, "section": title}
            ))
            idx += 1
        return chunks

class ParentChildChunker(BaseChunker):
    def __init__(self, parent_size: int = 800, child_size: int = 200):
        self.parent_size = parent_size
        self.child_size = child_size

    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[RawChunk]:
        words = text.split()
        chunks = []
        parent_idx = 0
        chunk_idx = 0
        i = 0
        while i < len(words):
            p_words = words[i : i + self.parent_size]
            p_text = " ".join(p_words)
            chunks.append(RawChunk(
                content=p_text,
                chunk_index=chunk_idx,
                token_count=self.estimate_tokens(p_text),
                strategy=ChunkingStrategy.PARENT_CHILD,
                metadata={**metadata, "is_parent": True, "parent_id": parent_idx}
            ))
            parent_chunk_idx = chunk_idx
            chunk_idx += 1
            
            j = 0
            while j < len(p_words):
                c_words = p_words[j : j + self.child_size]
                c_text = " ".join(c_words)
                chunks.append(RawChunk(
                    content=c_text,
                    chunk_index=chunk_idx,
                    token_count=self.estimate_tokens(c_text),
                    strategy=ChunkingStrategy.PARENT_CHILD,
                    parent_chunk_index=parent_chunk_idx,
                    metadata={**metadata, "is_parent": False, "parent_ref": parent_chunk_idx}
                ))
                chunk_idx += 1
                j += self.child_size
            i += self.parent_size
            parent_idx += 1
        return chunks

class CodeASTChunker(BaseChunker):
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[RawChunk]:
        blocks = re.split(r"(?=(?:\n|^)(?:async\s+)?(?:def|class|function|func|type)\s+)", text)
        chunks = []
        idx = 0
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            sig_match = re.match(r"(?:async\s+)?(def|class|function|func)\s+([a-zA-Z0-9_]+)", block)
            symbol_name = sig_match.group(2) if sig_match else f"block_{idx}"
            chunks.append(RawChunk(
                content=block,
                chunk_index=idx,
                token_count=self.estimate_tokens(block),
                strategy=ChunkingStrategy.CODE_AST,
                section_title=symbol_name,
                metadata={**metadata, "symbol": symbol_name}
            ))
            idx += 1
        return chunks
