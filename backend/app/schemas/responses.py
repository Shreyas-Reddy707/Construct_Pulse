from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class MessageResponse(BaseModel):
    """Simple response containing only a message."""
    message: str

class SuccessResponse(BaseModel, Generic[T]):
    """Standard generic success response envelope."""
    data: T
    message: Optional[str] = None

class ErrorModel(BaseModel):
    """Standard error detail model."""
    code: int
    message: str
    details: Optional[Any] = None
    request_id: Optional[str] = None

class ErrorResponse(BaseModel):
    """Standard generic error response envelope."""
    error: ErrorModel

class PaginationMetadata(BaseModel):
    """Standard pagination metadata."""
    total: int = Field(..., description="Total number of items across all pages")
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages available")

class PaginatedResponse(BaseModel, Generic[T]):
    """Standard generic paginated response envelope."""
    data: List[T]
    meta: PaginationMetadata
    message: Optional[str] = None

# --- API Helpers ---

def success(data: T, message: Optional[str] = None) -> SuccessResponse[T]:
    """Helper to build a standardized success response."""
    return SuccessResponse(data=data, message=message)

def error(code: int, message: str, details: Optional[Any] = None, request_id: Optional[str] = None) -> ErrorResponse:
    """Helper to build a standardized error response."""
    return ErrorResponse(error=ErrorModel(code=code, message=message, details=details, request_id=request_id))

def paginate(items: List[T], total: int, page: int, page_size: int, message: Optional[str] = None) -> PaginatedResponse[T]:
    """Helper to build a standardized paginated response."""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    meta = PaginationMetadata(
        total=total, 
        page=page, 
        page_size=page_size, 
        total_pages=total_pages
    )
    return PaginatedResponse(data=items, meta=meta, message=message)
