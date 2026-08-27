# ADR-005: Abstract Syntax Tree Parsing via Tree-Sitter and Python AST

## Status
ACCEPTED

## Context
Enterprise AI copilot operations require deterministic performance, zero hallucinations, strict security, and comprehensive auditability.

## Decision
We implement `Abstract Syntax Tree Parsing via Tree-Sitter and Python AST` as a first-class citizen in the AegisAI architecture.

## Consequences
- **Positive**: Guaranteed isolation, sub-second latency, deterministic root cause discovery.
- **Trade-offs**: Requires disciplined schema migrations and automated CI evaluation gates.
