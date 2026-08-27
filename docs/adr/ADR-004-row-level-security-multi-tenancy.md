# ADR-004: Multi-Tenancy via PostgreSQL Row-Level Security (RLS) & Tenant Middleware

## Status
Accepted

## Context
Enterprise clients demand strict tenant isolation preventing accidental cross-org document or code retrieval.

## Decision
Enforce `organization_id` on all database entities, inject `TenantContext` in middleware, and automatically inject tenant filters into all SQL and vector search queries.
