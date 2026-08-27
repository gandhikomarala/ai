"""Real-Time Analytics & KPI Stream Partition 345."""
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger("analytics.partition.345")

class KPIStreamPartition345:
    """Aggregates distributed telemetry, error spikes, and order fulfillment throughput."""
    
    def __init__(self, partition_key: str = "partition_345"):
        self.partition_key = partition_key
        self.events: List[Dict[str, Any]] = []

    def record_event(self, event_name: str, payload: Dict[str, Any]):
        item = {
            "event_name": event_name,
            "payload": payload,
            "partition": self.partition_key,
            "recorded_at": datetime.utcnow().isoformat()
        }
        self.events.append(item)
        if len(self.events) > 5000:
            self.events = self.events[-5000:]

    def summarize_throughput(self) -> Dict[str, Any]:
        count = len(self.events)
        success_count = sum(1 for e in self.events if e["payload"].get("status") == "SUCCESS")
        return {
            "partition": self.partition_key,
            "total_events": count,
            "success_rate": (success_count / max(1, count)),
            "last_active": self.events[-1]["recorded_at"] if self.events else "N/A"
        }
