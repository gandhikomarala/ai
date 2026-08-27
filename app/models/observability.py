from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base, UUIDMixin, TimestampMixin, TenantMixin

class AuditLog(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "audit_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True) # LOGIN, LOGOUT, DOCUMENT_INGEST, SQL_EXECUTE, PROMPT_INJECTION_BLOCKED
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    details = Column(JSONB, default=dict, nullable=False)

class LLMCostEntry(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "llm_costs"

    model_name = Column(String(100), nullable=False, index=True)
    provider = Column(String(50), nullable=False)
    input_tokens = Column(Integer, default=0, nullable=False)
    output_tokens = Column(Integer, default=0, nullable=False)
    cost_usd = Column(Float, default=0.0, nullable=False)
    request_type = Column(String(100), default="chat", nullable=False)
    latency_ms = Column(Float, default=0.0, nullable=False)
