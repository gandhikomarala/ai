from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

HTTP_REQUESTS_TOTAL = Counter(
    "aegisai_http_requests_total",
    "Total HTTP requests handled",
    ["method", "endpoint", "status"]
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "aegisai_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"]
)

RAG_REQUESTS_TOTAL = Counter(
    "aegisai_rag_requests_total",
    "Total RAG and agent queries processed",
    ["intent", "status"]
)

RAG_LATENCY_SECONDS = Histogram(
    "aegisai_rag_latency_seconds",
    "Latency of end-to-end RAG reasoning",
    ["intent"]
)

LLM_TOKENS_TOTAL = Counter(
    "aegisai_llm_tokens_total",
    "Total LLM tokens consumed",
    ["model", "type"]
)

LLM_COST_USD_TOTAL = Counter(
    "aegisai_llm_cost_usd_total",
    "Total accumulated LLM spend in USD",
    ["tenant", "model"]
)

ACTIVE_SESSIONS_GAUGE = Gauge(
    "aegisai_active_sessions",
    "Current active user sessions"
)

PROMPT_INJECTIONS_BLOCKED = Counter(
    "aegisai_prompt_injections_blocked_total",
    "Total prompt injection attacks intercepted"
)

def get_metrics_output():
    return generate_latest(), CONTENT_TYPE_LATEST
