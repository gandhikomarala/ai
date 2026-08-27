from typing import List, Dict, Any
from pydantic import BaseModel

class CitationItem(BaseModel):
    index: int
    source_type: str
    title: str
    file_path: str = ""
    section_title: str = ""
    start_line: int = 1
    end_line: int = 1
    snippet: str
    relevance_score: float = 1.0

class CitationEngine:
    def generate_citations(self, evidence_chunks: List[Any]) -> List[CitationItem]:
        citations = []
        for i, chunk in enumerate(evidence_chunks):
            meta = getattr(chunk, "metadata", {})
            citations.append(CitationItem(
                index=i + 1,
                source_type=meta.get("type", "document"),
                title=getattr(chunk, "title", "Document"),
                file_path=meta.get("file_path", ""),
                section_title=meta.get("section", ""),
                start_line=meta.get("start_line", 1),
                end_line=meta.get("end_line", 20),
                snippet=getattr(chunk, "content", "")[:200],
                relevance_score=float(getattr(chunk, "score", 1.0))
            ))
        return citations

citation_engine = CitationEngine()
