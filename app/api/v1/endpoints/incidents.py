from fastapi import APIRouter
from app.incidents.rca_engine import incident_rca_engine
from app.core.responses import success_response

router = APIRouter()

@router.get("/")
async def list_incidents():
    return success_response([
        {
            "id": "inc_001",
            "incident_key": "INC-2841",
            "title": "Payment API elevated 500 error storm",
            "severity": "CRITICAL",
            "status": "INVESTIGATING",
            "service": "payment-service",
            "started_at": "2026-08-27T08:15:00Z"
        }
    ])

@router.get("/{incident_key}/investigate")
async def investigate_incident(incident_key: str):
    rca = await incident_rca_engine.investigate_incident({"incident_key": incident_key, "service": "payment-service"})
    return success_response(rca)
