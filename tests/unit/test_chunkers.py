from app.ingestion.chunkers.smart_chunkers import FixedSizeChunker, SentenceChunker, MarkdownChunker, ParentChildChunker

def test_fixed_chunker():
    chunker = FixedSizeChunker(chunk_size=10, overlap=2)
    text = "word " * 50
    chunks = chunker.chunk(text, metadata={})
    assert len(chunks) > 1
    assert chunks[0].token_count > 0

def test_sentence_chunker():
    chunker = SentenceChunker(max_tokens=20)
    text = "First sentence here. Second sentence is longer. Third sentence completes the paragraph."
    chunks = chunker.chunk(text, metadata={})
    assert len(chunks) >= 1

def test_markdown_chunker():
    chunker = MarkdownChunker()
    md = "# Architecture\nThis is arch doc.\n## Payments\nThis is payment service."
    chunks = chunker.chunk(md, metadata={})
    assert len(chunks) >= 2
    assert chunks[0].section_title in ["Architecture", "Payments"]
