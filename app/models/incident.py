from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, DateTime, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin
from app.core.constants import IncidentSeverity, IncidentStatus

class Incident(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "incidents"

    incident_key = Column(String(50), unique=True, nullable=False, index=True) # e.g. INC-2841
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(SQLEnum(IncidentSeverity), default=IncidentSeverity.HIGH, nullable=False, index=True)
    status = Column(SQLEnum(IncidentStatus), default=IncidentStatus.DETECTED, nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=False, index=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    affected_services = Column(JSONB, default=list, nullable=False)
    root_cause_analysis = Column(Text, nullable=True)
    remediation_steps = Column(JSONB, default=list, nullable=False)
    confidence_score = Column(Float, default=0.0, nullable=False)

    project = relationship("Project", back_populates="incidents")
    events = relationship("IncidentEvent", back_populates="incident", cascade="all, delete-orphan")
    evidence = relationship("IncidentEvidence", back_populates="incident", cascade="all, delete-orphan")

class IncidentEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "incident_events"

    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False) # deployment, log_spike, alert, config_change
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    occurred_at = Column(DateTime(timezone=True), nullable=False, index=True)
    source_ref = Column(String(255), nullable=True) # commit_sha, deployment_id, log_trace_id
    metadata_ = Column("metadata", JSONB, default=dict, nullable=False)

    incident = relationship("Incident", back_populates="events")

class IncidentEvidence(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "incident_evidence"

    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_type = Column(String(100), nullable=False) # code_diff, stack_trace, log_anomaly, metric_spike
    title = Column(String(500), nullable=False)
    snippet = Column(Text, nullable=False)
    weight = Column(Float, default=1.0, nullable=False)
    relevance_rationale = Column(Text, nullable=True)
    source_pointer = Column(String(500), nullable=False)

    incident = relationship("Incident", back_populates="evidence")

class Deployment(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "deployments"

    service_name = Column(String(100), nullable=False, index=True)
    version = Column(String(50), nullable=False)
    environment = Column(String(50), default="production", nullable=False, index=True)
    deployed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    git_commit_sha = Column(String(64), nullable=False, index=True)
    status = Column(String(50), default="SUCCESS", nullable=False)
    changelog = Column(Text, nullable=True)

class LogEntry(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "logs"

    service_name = Column(String(100), nullable=False, index=True)
    environment = Column(String(50), default="production", nullable=False)
    level = Column(String(20), default="ERROR", nullable=False, index=True)
    message = Column(Text, nullable=False)
    trace_id = Column(String(100), nullable=True, index=True)
    span_id = Column(String(100), nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    stack_trace = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSONB, default=dict, nullable=False)
