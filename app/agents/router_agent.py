import re
from app.core.constants import AgentIntent

class RouterAgent:
    def classify_intent(self, query: str) -> AgentIntent:
        q = query.lower().strip()
        
        # 1. Incident
        if re.search(r"\b(inc-\d+|incident|500 error|outage|root cause|blast radius|rca)\b", q):
            return AgentIntent.INCIDENT
            
        # 2. SQL
        if re.search(r"\b(select|from|where|count|database schema|sql query|show failed payments|failed payments)\b", q):
            return AgentIntent.SQL
            
        # 3. Git
        if re.search(r"\b(commit|pull request|pr\s*#|diff|branch|git log|release\s*\d+)\b", q):
            return AgentIntent.GIT
            
        # 4. Code AST
        if re.search(r"\b(function|class|method|imports?|def\s+|ast|codebase|syntax|symbols?)\b", q):
            return AgentIntent.CODE
            
        # 5. Architecture / Service topology
        if re.search(r"\b(service topology|service dependencies|service dependency|microservice topology|architecture graph)\b", q):
            return AgentIntent.ARCHITECTURE
            
        # 6. Logs (word boundary so 'topology' is not matched)
        if re.search(r"\b(logs?|stacktrace|exception|error spike|trace_id|timestamp)\b", q):
            return AgentIntent.LOGS
            
        # 7. Default Knowledge Base & Architecture Q&A
        return AgentIntent.KNOWLEDGE

router_agent = RouterAgent()
