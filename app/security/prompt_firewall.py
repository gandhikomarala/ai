import re
from typing import Tuple, List
from app.core.exceptions import PromptInjectionDetected

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"you\s+are\s+now\s+in\s+DAN\s+mode",
    r"disregard\s+system\s+prompt",
    r"system\s*:\s*override",
    r"reveal\s+your\s+(initial|system)\s+instructions",
    r"output\s+all\s+confidential\s+data",
    r"<\s*script\s*>",
    r"\[\s*system\s*\]\s*:",
    r"print\s+environment\s+variables",
    r"format\s+drive\s+c:",
]

class PromptFirewall:
    def __init__(self):
        self.compiled_rules = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

    def inspect_user_input(self, text: str) -> Tuple[bool, str]:
        for pattern in self.compiled_rules:
            if pattern.search(text):
                return False, f"Prompt injection pattern matched: '{pattern.pattern}'"
        return True, "Passed"

    def sanitize_retrieved_context(self, context_chunks: List[str]) -> List[str]:
        sanitized = []
        for chunk in context_chunks:
            # Neutralize instruction injection in retrieved documents
            neutralized = re.sub(r"(?i)(ignore previous instructions|system prompt:)", "[REDACTED_INSTRUCTION]", chunk)
            sanitized.append(neutralized)
        return sanitized

prompt_firewall = PromptFirewall()
