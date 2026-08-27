from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, Float, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from app.db.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin
from app.core.constants import DocumentType, ChunkingStrategy

class Document(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "documents"

    title = Column(String(500), nullable=False, index=True)
    source_url = Column(String(1000), nullable=True)
    file_path = Column(String(1000), nullable=True)
    mime_type = Column(String(100), nullable=False)
    doc_type = Column(SQLEnum(DocumentType), default=DocumentType.TEXT, nullable=False)
    sha256_hash = Column(String(64), nullable=False, index=True)
    size_bytes = Column(Integer, nullable=False)
    metadata_ = Column("metadata", JSONB, default=dict, nullable=False)
    is_indexed = Column(Boolean, default=False, nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)

    project = relationship("Project", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentVersion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "document_versions"

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    storage_path = Column(String(1000), nullable=False)
    changes_summary = Column(Text, nullable=True)

    document = relationship("Document", back_populates="versions")

class DocumentChunk(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "document_chunks"

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id", ondelete="SET NULL"), nullable=True, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=False)
    strategy = Column(SQLEnum(ChunkingStrategy), default=ChunkingStrategy.SEMANTIC, nullable=False)
    page_number = Column(Integer, nullable=True)
    section_title = Column(String(500), nullable=True)
    language = Column(String(50), default="en", nullable=False)
    metadata_ = Column("metadata", JSONB, default=dict, nullable=False)

    document = relationship("Document", back_populates="chunks")
    embeddings = relationship("Embedding", back_populates="chunk", cascade="all, delete-orphan")

class Embedding(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "embeddings"

    chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False, index=True)
    model_name = Column(String(100), nullable=False)
    dimension = Column(Integer, default=1536, nullable=False)
    vector = Column(Vector(1536), nullable=False)

    chunk = relationship("DocumentChunk", back_populates="embeddings")
