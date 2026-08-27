from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin
from app.core.constants import AgentIntent

class Conversation(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "conversations"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), default="New Investigation", nullable=False)
    context_summary = Column(Text, nullable=True)
    session_metadata = Column(JSONB, default=dict, nullable=False)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")

class Message(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "messages"

    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False) # user, assistant, system, tool
    content = Column(Text, nullable=False)
    intent = Column(SQLEnum(AgentIntent), default=AgentIntent.KNOWLEDGE, nullable=True)
    token_count = Column(Integer, default=0, nullable=False)
    cost_usd = Column(Float, default=0.0, nullable=False)
    agent_steps = Column(JSONB, default=list, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    citations = relationship("Citation", back_populates="message", cascade="all, delete-orphan")
    feedback = relationship("UserFeedback", back_populates="message", uselist=False, cascade="all, delete-orphan")

class Citation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "citations"

    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, index=True)
    source_type = Column(String(50), nullable=False) # document, code, commit, incident, runbook
    title = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=True)
    section_title = Column(String(500), nullable=True)
    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)
    page_number = Column(Integer, nullable=True)
    commit_sha = Column(String(64), nullable=True)
    snippet = Column(Text, nullable=False)
    relevance_score = Column(Float, default=1.0, nullable=False)

    message = relationship("Message", back_populates="citations")

class UserFeedback(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "feedback"

    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, unique=True)
    rating = Column(Integer, nullable=False) # 1 (up) or -1 (down)
    comment = Column(Text, nullable=True)
    corrected_answer = Column(Text, nullable=True)

    message = relationship("Message", back_populates="feedback")
