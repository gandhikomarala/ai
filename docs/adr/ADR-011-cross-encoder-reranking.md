# ADR-011: Two-Stage Retrieval with Cross-Encoder Scoring

## Status
ACCEPTED

## Context
Enterprise AI copilot operations require deterministic performance, zero hallucinations, strict security, and comprehensive auditability.

## Decision
We implement `Two-Stage Retrieval with Cross-Encoder Scoring` as a first-class citizen in the AegisAI architecture.

## Consequences
- **Positive**: Guaranteed isolation, sub-second latency, deterministic root cause discovery.
- **Trade-offs**: Requires disciplined schema migrations and automated CI evaluation gates.
