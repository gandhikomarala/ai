# ADR-003: LangGraph Multi-Agent Orchestration

## Status
Accepted

## Context
Complex incident root cause analysis requires multi-step reasoning: timeline reconstruction, log clustering, commit diff blame, and SQL verification.

## Decision
Implement a deterministic LangGraph StateGraph runtime with step budgeting, timeout guards, and strict evidence validation before response streaming.
