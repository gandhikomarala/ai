import pytest
from uuid import uuid4
from app.agents.runtime import agent_runtime
from app.security.tenant import TenantContext
from app.core.exceptions import TenantIsolationViolation

@pytest.mark.asyncio
async def test_scenario_1_document_qa():
    state = await agent_runtime.execute("What is our authentication architecture?")
    assert state.is_safe
    assert len(state.final_answer) > 0
    assert len(state.citations) >= 1

@pytest.mark.asyncio
async def test_scenario_2_git_code_search():
    state = await agent_runtime.execute("Show function signature for execute_charge in payment processor")
    assert state.is_safe
    assert len(state.steps) >= 1

@pytest.mark.asyncio
async def test_scenario_3_incident_investigation_rca():
    state = await agent_runtime.execute("Why did incident INC-2841 happen?")
    assert state.is_safe
    assert "INC-2841" in state.final_answer
    assert "stripe_customer_id" in state.final_answer or "migration" in state.final_answer

@pytest.mark.asyncio
async def test_scenario_4_safe_sql_query():
    state = await agent_runtime.execute("Show failed payments in database")
    assert state.is_safe
    assert "SELECT" in state.final_answer

def test_scenario_5_cross_tenant_access_denied():
    org_a = uuid4()
    org_b = uuid4()
    ctx = TenantContext(organization_id=org_a)
    with pytest.raises(TenantIsolationViolation):
        ctx.validate_access(target_org_id=org_b)
