from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.constants import AgentIntent

class AgentStep(BaseModel):
    step_number: int
    agent_name: str
    action: str
    thought: str
    observation: str
    latency_ms: float = 0.0

class AgentState(BaseModel):
    query: str
    intent: AgentIntent = AgentIntent.KNOWLEDGE
    context_chunks: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    steps: List[AgentStep] = Field(default_factory=list)
    final_answer: str = ""
    confidence: float = 1.0
    execution_time_ms: float = 0.0
    is_safe: bool = True
