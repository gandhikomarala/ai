from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
from app.agents.runtime import agent_runtime
from app.core.responses import success_response

router = APIRouter()

class ChatQueryRequest(BaseModel):
    query: str
    conversation_id: str = "conv_default"

@router.post("/query")
async def query_copilot(req: ChatQueryRequest):
    state = await agent_runtime.execute(req.query)
    return success_response(state.model_dump())

@router.post("/stream")
async def stream_copilot(req: ChatQueryRequest):
    async def event_generator():
        yield f"data: {json.dumps({'event': 'thought', 'content': 'Classifying query intent...'})}\n\n"
        await asyncio.sleep(0.1)
        state = await agent_runtime.execute(req.query)
        for step in state.steps:
            yield f"data: {json.dumps({'event': 'step', 'agent': step.agent_name, 'action': step.action, 'thought': step.thought})}\n\n"
            await asyncio.sleep(0.05)
        words = state.final_answer.split()
        for w in words:
            yield f"data: {json.dumps({'event': 'token', 'text': w + ' '})}\n\n"
            await asyncio.sleep(0.02)
        yield f"data: {json.dumps({'event': 'citations', 'citations': state.citations})}\n\n"
        yield f"data: {json.dumps({'event': 'done', 'execution_time_ms': state.execution_time_ms})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
