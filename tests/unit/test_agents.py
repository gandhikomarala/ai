import pytest
from app.agents.router_agent import router_agent
from app.agents.runtime import agent_runtime
from app.core.constants import AgentIntent

def test_router_classification():
    assert router_agent.classify_intent("Why did INC-2841 fail?") == AgentIntent.INCIDENT
    assert router_agent.classify_intent("SELECT * FROM payments WHERE status = 'FAILED'") == AgentIntent.SQL
    assert router_agent.classify_intent("What changed in commit abc1234?") == AgentIntent.GIT
    assert router_agent.classify_intent("What is our authentication architecture?") == AgentIntent.KNOWLEDGE

@pytest.mark.asyncio
async def test_agent_runtime_knowledge_execution():
    state = await agent_runtime.execute("What is our authentication architecture?")
    assert state.is_safe
    assert len(state.steps) >= 1
    assert len(state.final_answer) > 0
