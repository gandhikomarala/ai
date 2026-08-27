from typing import List, Dict, Any

class PagerDutyConnector:
    """Integrates alert webhooks and incident streams."""
    
    async def fetch_active_alerts(self) -> List[Dict[str, Any]]:
        return [
            {
                "alert_id": "ALT-90412",
                "incident_key": "INC-2841",
                "service": "payment-service",
                "severity": "CRITICAL",
                "summary": "Elevated 500 HTTP errors on /api/v1/charges exceeded 15% threshold",
                "created_at": "2026-08-27T08:15:00Z"
            }
        ]

pagerduty_connector = PagerDutyConnector()
