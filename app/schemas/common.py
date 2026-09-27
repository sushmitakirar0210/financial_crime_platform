from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar("T")

class StatusResponse(BaseModel):
    """Standard generic response for operation status messages."""
    status: str = "success"
    message: str

class ErrorResponse(BaseModel):
    """Standardized structure for API error responses."""
    status: str = "error"
    detail: str
    code: Optional[int] = None

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic wrapper for paginated API list responses."""
    total: int
    page: int
    size: int
    items: list[T]