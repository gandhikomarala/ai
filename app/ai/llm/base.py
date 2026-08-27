from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List, Optional
from pydantic import BaseModel, Field

class LLMMessage(BaseModel):
    role: str # system, user, assistant, tool
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

class LLMResponse(BaseModel):
    content: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[LLMMessage], model: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2000) -> LLMResponse:
        pass

    @abstractmethod
    async def generate_stream(self, messages: List[LLMMessage], model: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 2000) -> AsyncGenerator[str, None]:
        pass
