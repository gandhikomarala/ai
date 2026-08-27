from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base, UUIDMixin, TimestampMixin, TenantMixin

class EvaluationDataset(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "evaluation_datasets"

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    domain = Column(String(100), default="engineering", nullable=False)
    version = Column(Integer, default=1, nullable=False)

    questions = relationship("EvaluationQuestion", back_populates="dataset", cascade="all, delete-orphan")
    runs = relationship("EvaluationRun", back_populates="dataset", cascade="all, delete-orphan")

class EvaluationQuestion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "evaluation_questions"

    dataset_id = Column(UUID(as_uuid=True), ForeignKey("evaluation_datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    ground_truth = Column(Text, nullable=False)
    expected_sources = Column(JSONB, default=list, nullable=False)
    difficulty = Column(String(50), default="medium", nullable=False)
    category = Column(String(100), default="knowledge", nullable=False)

    dataset = relationship("EvaluationDataset", back_populates="questions")

class EvaluationRun(Base, UUIDMixin, TimestampMixin, TenantMixin):
    __tablename__ = "evaluation_runs"

    dataset_id = Column(UUID(as_uuid=True), ForeignKey("evaluation_datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    run_name = Column(String(255), nullable=False)
    git_commit_sha = Column(String(64), nullable=True)
    overall_faithfulness = Column(Float, default=0.0, nullable=False)
    overall_context_recall = Column(Float, default=0.0, nullable=False)
    overall_answer_relevance = Column(Float, default=0.0, nullable=False)
    overall_citation_accuracy = Column(Float, default=0.0, nullable=False)
    passed_regression_gate = Column(Boolean, default=True, nullable=False)
    summary_metrics = Column(JSONB, default=dict, nullable=False)

    dataset = relationship("EvaluationDataset", back_populates="runs")
    results = relationship("EvaluationResult", back_populates="run", cascade="all, delete-orphan")

class EvaluationResult(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "evaluation_results"

    run_id = Column(UUID(as_uuid=True), ForeignKey("evaluation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("evaluation_questions.id", ondelete="CASCADE"), nullable=False)
    generated_answer = Column(Text, nullable=False)
    faithfulness_score = Column(Float, nullable=False)
    context_recall_score = Column(Float, nullable=False)
    answer_relevance_score = Column(Float, nullable=False)
    citation_accuracy_score = Column(Float, nullable=False)
    latency_ms = Column(Float, nullable=False)
    token_usage = Column(Integer, nullable=False)

    run = relationship("EvaluationRun", back_populates="results")
