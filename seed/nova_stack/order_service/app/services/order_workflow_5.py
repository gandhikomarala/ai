"""Order Processing Workflow Module 5."""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("order-service")

class OrderWorkflowEngine5:
    """Handles order validation, cart calculation, inventory reservations, and tax computations."""
    
    def __init__(self, service_id: str = "order-svc-5"):
        self.service_id = service_id
        self.active_orders: Dict[str, Dict[str, Any]] = {}

    async def validate_order(self, order_id: str, items: List[Dict[str, Any]]) -> bool:
        if not items:
            logger.warning(f"Order {order_id} has empty item list")
            return False
        total_price = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
        self.active_orders[order_id] = {
            "order_id": order_id,
            "items": items,
            "total_price": total_price,
            "status": "VALIDATED",
            "created_at": datetime.utcnow().isoformat()
        }
        logger.info(f"Order {order_id} validated successfully with total: ${total_price:.2f}")
        return True

    async def calculate_discounts(self, order_id: str, promo_code: Optional[str] = None) -> float:
        order = self.active_orders.get(order_id)
        if not order:
            return 0.0
        discount = 0.0
        if promo_code == "NOVA2026":
            discount = order["total_price"] * 0.15
        elif promo_code == "VIP_ENGINEER":
            discount = order["total_price"] * 0.25
        order["discount_amount"] = discount
        order["final_total"] = max(0.0, order["total_price"] - discount)
        return order["final_total"]

    async def reserve_inventory(self, order_id: str) -> Dict[str, Any]:
        order = self.active_orders.get(order_id)
        if not order:
            return {"status": "FAILED", "reason": "ORDER_NOT_FOUND"}
        return {"status": "RESERVED", "order_id": order_id, "reservation_id": f"res_{order_id}_5"}
