from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ORG_ADMIN = "ORG_ADMIN"
    PROJECT_ADMIN = "PROJECT_ADMIN"
    ENGINEER = "ENGINEER"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"

class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    MARKDOWN = "markdown"
    TEXT = "text"
    HTML = "html"
    CSV = "csv"
    JSON = "json"
    YAML = "yaml"
    CODE = "code"
    OPENAPI = "openapi"
    TERRAFORM = "terraform"
    DOCKERFILE = "dockerfile"
    SQL = "sql"
    RUNBOOK = "runbook"

class ChunkingStrategy(str, Enum):
    FIXED = "fixed"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    MARKDOWN = "markdown"
    SECTION = "section"
    PARENT_CHILD = "parent_child"
    CODE_AST = "code_ast"

class AgentIntent(str, Enum):
    KNOWLEDGE = "knowledge"
    CODE = "code"
    GIT = "git"
    INCIDENT = "incident"
    SQL = "sql"
    LOGS = "logs"
    ARCHITECTURE = "architecture"
    MULTI_STEP = "multi_step"

class IncidentSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    IDENTIFIED = "IDENTIFIED"
    MITIGATING = "MITIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    NVIDIA = "nvidia"
    OLLAMA = "ollama"
    LITELLM = "litellm"
    MOCK = "mock"
