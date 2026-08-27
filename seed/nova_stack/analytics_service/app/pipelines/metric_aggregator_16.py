"""Analytics & Financial KPI Aggregator Pipeline 16."""
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger("analytics-service")

class MetricAggregatorPipeline16:
    """Aggregates real-time financial metrics, payment failure rates, and service health statistics."""
    
    def __init__(self, partition_key: str = "daily_kpi_16"):
        self.partition_key = partition_key
        self.records: List[Dict[str, Any]] = []

    def ingest_transaction(self, tx_id: str, amount: float, status: str, service: str):
        record = {
            "transaction_id": tx_id,
            "amount": amount,
            "status": status,
            "service": service,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.records.append(record)
        if len(self.records) > 5000:
            self.records = self.records[-5000:]

    def compute_failure_rate(self) -> float:
        if not self.records:
            return 0.0
        failed = sum(1 for r in self.records if r["status"] == "FAILED")
        return round(failed / len(self.records), 4)

    def calculate_total_revenue(self) -> float:
        return sum(r["amount"] for r in self.records if r["status"] == "SUCCEEDED")
