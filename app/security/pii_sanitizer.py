import re
import math

class PIISanitizer:
    PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "PHONE": r"\b(?:\+?1[-.]?)?\(?[2-9]\d{2}\)?[-.]?\d{3}[-.]?\d{4}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "AWS_KEY": r"\b(AKIA|ASIA)[0-9A-Z]{12,24}\b",
        "GITHUB_TOKEN": r"\b(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}\b",
        "JWT_TOKEN": r"\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b",
        "API_KEY": r"(?i)(api_key|secret_key|password)\s*[:=]\s*['\"][a-zA-Z0-9_\-+=/]{16,}['\"]"
    }

    def __init__(self):
        self.compiled = {k: re.compile(v) for k, v in self.PATTERNS.items()}

    def sanitize(self, text: str) -> str:
        out = text
        for pii_type, regex in self.compiled.items():
            out = regex.sub(f"[REDACTED_{pii_type}]", out)
        return out

    def calculate_shannon_entropy(self, data: str) -> float:
        if not data:
            return 0.0
        entropy = 0.0
        for x in set(data):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log2(p_x)
        return entropy

pii_sanitizer = PIISanitizer()
