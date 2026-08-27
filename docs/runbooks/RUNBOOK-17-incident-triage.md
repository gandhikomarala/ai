# Production Runbook 17: Incident Triage & Root Cause Discovery

## Overview
Standard operating procedure for responding to Sev-1/Sev-2 telemetry alarms in NovaStack production environments.

## Triage Procedure
1. Query AegisAI Incident Copilot with incident key or error signature.
2. Inspect correlated git deployments in the preceding 60-minute window.
3. Verify database schema migration parity against active models.
4. Execute compensating rollback if migration drift or syntax errors are detected.
5. Notify on-call stakeholders via PagerDuty and Slack channel `#incident-room`.
