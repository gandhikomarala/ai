from typing import List, Dict, Any

class GraphRAGRetriever:
    def __init__(self):
        # Service dependency graph nodes & edges
        self.nodes = {
            "api-gateway": {"type": "Service", "team": "Platform"},
            "auth-service": {"type": "Service", "team": "Security"},
            "user-service": {"type": "Service", "team": "Core"},
            "payment-service": {"type": "Service", "team": "Billing"},
            "order-service": {"type": "Service", "team": "Commerce"},
            "notification-service": {"type": "Service", "team": "Engagement"},
            "analytics-service": {"type": "Service", "team": "Data"},
            "payments_db": {"type": "Database", "engine": "PostgreSQL"},
            "orders_db": {"type": "Database", "engine": "PostgreSQL"},
        }
        self.edges = [
            ("api-gateway", "auth-service", "AUTHENTICATES_WITH"),
            ("api-gateway", "order-service", "ROUTES_TO"),
            ("order-service", "payment-service", "CALLS_SYNC"),
            ("order-service", "notification-service", "EMITS_EVENT"),
            ("payment-service", "payments_db", "READS_WRITES"),
            ("order-service", "orders_db", "READS_WRITES")
        ]

    def get_service_dependencies(self, service_name: str) -> Dict[str, Any]:
        upstream = [src for src, tgt, rel in self.edges if tgt == service_name]
        downstream = [tgt for src, tgt, rel in self.edges if src == service_name]
        return {
            "service": service_name,
            "upstream_callers": upstream,
            "downstream_dependencies": downstream,
            "direct_relationships": [
                {"from": s, "to": t, "type": r} for s, t, r in self.edges if s == service_name or t == service_name
            ]
        }

graph_rag_retriever = GraphRAGRetriever()
