-- NovaStack Database Schema Evolution Migration 038
-- Author: AegisAI Platform Engineering Team

CREATE TABLE IF NOT EXISTS audit_event_ledger_038 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(100) NOT NULL,
    actor_id UUID NOT NULL,
    previous_state JSONB DEFAULT '{}'::jsonb NOT NULL,
    new_state JSONB DEFAULT '{}'::jsonb NOT NULL,
    correlation_id VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_038_entity ON audit_event_ledger_038(entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_038_corr ON audit_event_ledger_038(correlation_id);
CREATE INDEX IF NOT EXISTS idx_audit_038_created ON audit_event_ledger_038(created_at DESC);
