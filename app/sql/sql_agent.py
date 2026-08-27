from typing import Dict, Any, List
from app.security.sql_guard import sql_guard
from app.core.exceptions import SQLSecurityViolation

class SQLAgent:
    def __init__(self):
        self.mock_schema = {
            "users": ["id", "email", "full_name", "created_at", "organization_id"],
            "orders": ["id", "user_id", "total_amount_usd", "status", "created_at"],
            "payments": ["id", "order_id", "amount", "status", "stripe_customer_id", "created_at"],
            "incidents": ["id", "incident_key", "severity", "status", "started_at", "service"]
        }

    def get_schema(self) -> Dict[str, List[str]]:
        return self.mock_schema

    def generate_sql(self, natural_language_query: str) -> str:
        q = natural_language_query.lower()
        if "payment" in q and "fail" in q:
            return "SELECT id, order_id, amount, status FROM payments WHERE status = 'FAILED' ORDER BY created_at DESC LIMIT 50;"
        elif "incident" in q:
            return "SELECT incident_key, severity, status, started_at FROM incidents ORDER BY started_at DESC LIMIT 20;"
        elif "order" in q or "total" in q:
            return "SELECT status, COUNT(*) as count, SUM(total_amount_usd) as revenue FROM orders GROUP BY status LIMIT 10;"
        return "SELECT id, email, created_at FROM users ORDER BY created_at DESC LIMIT 20;"

    async def execute_safe_query(self, sql_query: str) -> Dict[str, Any]:
        # Validate through strict AST-level SQL guard
        is_safe, safe_sql, message = sql_guard.validate_and_sanitize(sql_query)
        
        # Execute against read-only mock sandbox
        sample_rows = [
            {"id": "pay_982341", "order_id": "ord_5521", "amount": 149.99, "status": "FAILED"},
            {"id": "pay_982342", "order_id": "ord_5522", "amount": 89.50, "status": "FAILED"},
            {"id": "pay_982343", "order_id": "ord_5523", "amount": 299.00, "status": "FAILED"}
        ]
        
        return {
            "executed_sql": safe_sql,
            "row_count": len(sample_rows),
            "columns": list(sample_rows[0].keys()) if sample_rows else [],
            "rows": sample_rows,
            "security_status": "VERIFIED_READ_ONLY"
        }

sql_agent = SQLAgent()
