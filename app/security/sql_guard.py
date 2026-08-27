import re
from typing import Tuple
from app.core.exceptions import SQLSecurityViolation

try:
    import sqlglot
    from sqlglot import exp
    HAS_SQLGLOT = True
except ImportError:
    HAS_SQLGLOT = False

FORBIDDEN_KEYWORDS = [
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|GRANT|REVOKE|EXEC|EXECUTE)\b",
    r"--",
    r";\s*\S+" # Disallow chained statements
]

class SQLGuard:
    def __init__(self, max_limit: int = 100):
        self.max_limit = max_limit

    def validate_and_sanitize(self, sql_query: str) -> Tuple[bool, str, str]:
        cleaned = re.sub(r"--.*$", "", sql_query, flags=re.MULTILINE).strip()
        if not cleaned:
            raise SQLSecurityViolation("Empty SQL query provided")

        # Fallback regex-based AST scanner when sqlglot is not present in local env
        if not HAS_SQLGLOT:
            # Check for multiple statements
            statements = [s.strip() for s in cleaned.split(";") if s.strip()]
            if len(statements) > 1:
                raise SQLSecurityViolation("Multiple SQL statements in a single execution are forbidden")
            
            stmt = statements[0]
            if not stmt.upper().startswith("SELECT"):
                raise SQLSecurityViolation(f"Only SELECT statements are permitted. Detected non-SELECT query.")

            for pattern in FORBIDDEN_KEYWORDS:
                if re.search(pattern, stmt, re.IGNORECASE):
                    raise SQLSecurityViolation(f"Forbidden SQL operation or pattern detected")

            # Check/Enforce LIMIT
            if not re.search(r"\bLIMIT\s+\d+", stmt, re.IGNORECASE):
                stmt += f" LIMIT {self.max_limit}"
            else:
                # Replace higher limits with max_limit
                match = re.search(r"\bLIMIT\s+(\d+)", stmt, re.IGNORECASE)
                if match and int(match.group(1)) > self.max_limit:
                    stmt = re.sub(r"\bLIMIT\s+\d+", f"LIMIT {self.max_limit}", stmt, flags=re.IGNORECASE)

            return True, stmt, "Query passed all security checks (heuristic engine)"

        # sqlglot-based full AST parser
        try:
            parsed_trees = sqlglot.parse(cleaned, read="postgres")
        except Exception as e:
            raise SQLSecurityViolation(f"SQL Syntax Error: {str(e)}")

        if len(parsed_trees) != 1:
            raise SQLSecurityViolation("Multiple SQL statements in a single execution are forbidden")

        tree = parsed_trees[0]
        if not isinstance(tree, exp.Select):
            raise SQLSecurityViolation(f"Only SELECT statements are permitted. Detected: {type(tree).__name__}")

        limit_node = tree.find(exp.Limit)
        if limit_node:
            limit_val = int(limit_node.expression.this)
            if limit_val > self.max_limit:
                limit_node.set("this", exp.Literal.number(self.max_limit))
        else:
            tree = tree.limit(self.max_limit)

        return True, tree.sql(dialect="postgres"), "Query passed all security checks"

sql_guard = SQLGuard()
