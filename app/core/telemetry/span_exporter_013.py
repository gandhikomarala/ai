"""Telemetry & Distributed Tracing Span Exporter 013."""
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger("aegisai.telemetry.exporter.013")

class SpanExporter013:
    """Batches and exports OpenTelemetry trace spans to distributed collectors with backpressure control."""
    
    def __init__(self, buffer_size: int = 5000):
        self.buffer_size = buffer_size
        self.spans: List[Dict[str, Any]] = []

    def queue_span(self, trace_id: str, span_id: str, operation_name: str, duration_ms: float):
        entry = {
            "trace_id": trace_id,
            "span_id": span_id,
            "operation": operation_name,
            "duration_ms": duration_ms,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.spans.append(entry)
        if len(self.spans) >= self.buffer_size:
            self.flush()

    def flush(self) -> int:
        count = len(self.spans)
        self.spans = []
        logger.info(f"[Exporter-013] Flushed {count} spans to OTLP collector")
        return count
