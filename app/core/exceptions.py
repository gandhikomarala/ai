from typing import Any, Dict, Optional

class AegisAIException(Exception):
    """Base application exception."""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class AuthenticationError(AegisAIException):
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=401, details=details)

class AuthorizationError(AegisAIException):
    def __init__(self, message: str = "Access denied: insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=403, details=details)

class TenantIsolationViolation(AegisAIException):
    def __init__(self, message: str = "Access denied: cross-tenant boundary breach attempted", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=403, details=details)

class ResourceNotFoundError(AegisAIException):
    def __init__(self, resource: str, identifier: Any, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=f"{resource} with identifier '{identifier}' not found", status_code=404, details=details)

class ValidationError(AegisAIException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, details=details)

class PromptInjectionDetected(AegisAIException):
    def __init__(self, message: str = "Security alert: potential prompt injection pattern blocked", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=400, details=details)

class SQLSecurityViolation(AegisAIException):
    def __init__(self, message: str = "SQL security violation: only safe read-only SELECT queries are permitted", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=400, details=details)

class LLMProviderError(AegisAIException):
    def __init__(self, provider: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=f"LLM Provider [{provider}] error: {message}", status_code=502, details=details)

class IngestionError(AegisAIException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=400, details=details)
