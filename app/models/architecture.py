from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base, UUIDMixin, TimestampMixin, TenantMixin

class Service(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "services"

    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    tier = Column(String(50), default="backend", nullable=False)
    language = Column(String(50), default="python", nullable=False)
    owner_team = Column(String(100), default="Core Platform", nullable=False)
    repo_url = Column(String(1000), nullable=True)
    health_status = Column(String(50), default="HEALTHY", nullable=False)
    endpoints = Column(JSONB, default=list, nullable=False)

    outgoing_dependencies = relationship("ServiceDependency", foreign_keys="ServiceDependency.source_service_id", back_populates="source_service", cascade="all, delete-orphan")
    incoming_dependencies = relationship("ServiceDependency", foreign_keys="ServiceDependency.target_service_id", back_populates="target_service", cascade="all, delete-orphan")

class ServiceDependency(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "service_dependencies"

    source_service_id = Column(UUID(as_uuid=True), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    target_service_id = Column(UUID(as_uuid=True), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    dependency_type = Column(String(50), default="HTTP_SYNC", nullable=False) # HTTP_SYNC, ASYNC_QUEUE, DB_SHARED
    is_critical = Column(Boolean, default=True, nullable=False)

    source_service = relationship("Service", foreign_keys=[source_service_id], back_populates="outgoing_dependencies")
    target_service = relationship("Service", foreign_keys=[target_service_id], back_populates="incoming_dependencies")
