from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin

class Repository(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "repositories"

    name = Column(String(255), nullable=False, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    provider = Column(String(50), default="github", nullable=False)
    remote_url = Column(String(1000), nullable=False)
    default_branch = Column(String(100), default="main", nullable=False)
    is_private = Column(Boolean, default=True, nullable=False)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    settings = Column(JSONB, default=dict, nullable=False)

    project = relationship("Project", back_populates="repositories")
    files = relationship("RepositoryFile", back_populates="repository", cascade="all, delete-orphan")
    commits = relationship("Commit", back_populates="repository", cascade="all, delete-orphan")
    pull_requests = relationship("PullRequest", back_populates="repository", cascade="all, delete-orphan")

class RepositoryFile(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "repository_files"

    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    path = Column(String(1000), nullable=False, index=True)
    language = Column(String(50), nullable=False, index=True)
    content = Column(Text, nullable=False)
    sha = Column(String(64), nullable=False)
    loc = Column(Integer, default=0, nullable=False)
    ast_summary = Column(JSONB, default=dict, nullable=False)

    repository = relationship("Repository", back_populates="files")
    symbols = relationship("CodeSymbol", back_populates="file", cascade="all, delete-orphan")

class CodeSymbol(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "code_symbols"

    file_id = Column(UUID(as_uuid=True), ForeignKey("repository_files.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    symbol_type = Column(String(50), nullable=False, index=True) # function, class, method, route
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)
    signature = Column(String(1000), nullable=True)
    docstring = Column(Text, nullable=True)
    references = Column(JSONB, default=list, nullable=False)

    file = relationship("RepositoryFile", back_populates="symbols")

class Commit(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "commits"

    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    sha = Column(String(64), nullable=False, index=True)
    message = Column(Text, nullable=False)
    author_name = Column(String(255), nullable=False)
    author_email = Column(String(255), nullable=False)
    committed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    diff_stats = Column(JSONB, default=dict, nullable=False)

    repository = relationship("Repository", back_populates="commits")

class PullRequest(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "pull_requests"

    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    pr_number = Column(Integer, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String(50), default="open", nullable=False)
    source_branch = Column(String(100), nullable=False)
    target_branch = Column(String(100), default="main", nullable=False)
    merged_at = Column(DateTime(timezone=True), nullable=True)

    repository = relationship("Repository", back_populates="pull_requests")
