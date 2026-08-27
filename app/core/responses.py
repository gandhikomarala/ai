from typing import Generic, TypeVar, Optional, Any, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime, timezone

T = TypeVar("T")

class MetaInfo(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: Optional[str] = None
    execution_time_ms: Optional[float] = None

class PaginationInfo(BaseModel):
    page: int = 1
    page_size: int = 20
    total_count: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    meta: MetaInfo = Field(default_factory=MetaInfo)
    error: Optional[Dict[str, Any]] = None

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: List[T] = Field(default_factory=list)
    pagination: PaginationInfo
    meta: MetaInfo = Field(default_factory=MetaInfo)
    error: Optional[Dict[str, Any]] = None

def success_response(data: Any, request_id: Optional[str] = None, exec_time_ms: Optional[float] = None) -> APIResponse:
    meta = MetaInfo(request_id=request_id, execution_time_ms=exec_time_ms)
    return APIResponse(success=True, data=data, meta=meta)

def error_response(message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None) -> APIResponse:
    meta = MetaInfo(request_id=request_id)
    return APIResponse(
        success=False,
        data=None,
        meta=meta,
        error={"code": status_code, "message": message, "details": details or {}}
    )
