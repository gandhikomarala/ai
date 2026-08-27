import logging
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger("payment-service")

app = FastAPI(title="NovaStack Payment Service", version="2.8.0")

class ChargeRequest(BaseModel):
    order_id: str
    amount_cents: int
    currency: str = "usd"
    customer_id: str

class ChargeResponse(BaseModel):
    charge_id: str
    order_id: str
    status: str
    amount_cents: int
    created_at: str

@app.get("/health")
async def health():
    return {"status": "HEALTHY", "version": "2.8.0", "database": "CONNECTED"}

@app.post("/api/v1/charges", response_model=ChargeResponse)
async def create_charge(req: ChargeRequest, authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    logger.info(f"Processing payment charge for order: {req.order_id} customer: {req.customer_id}")
    # Simulating the bug: if database migration 042 was not run, this query triggers 500 error
    return ChargeResponse(
        charge_id=f"ch_{int(datetime.now().timestamp())}",
        order_id=req.order_id,
        status="SUCCEEDED",
        amount_cents=req.amount_cents,
        created_at=datetime.utcnow().isoformat()
    )

@app.post("/api/v1/webhooks/stripe")
async def stripe_webhook(payload: dict):
    event_type = payload.get("type", "unknown")
    logger.info(f"Received Stripe webhook event: {event_type}")
    return {"status": "ACKNOWLEDGED"}
