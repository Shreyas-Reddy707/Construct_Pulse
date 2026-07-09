from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging import get_logger

logger = get_logger("constructpulse.exceptions")


# ─── Domain Exceptions ────────────────────────────────────────────────────────

class DomainException(Exception):
    """
    Base class for all domain-level business exceptions.
    These exceptions should be caught by the API layer and translated 
    into appropriate HTTP responses.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationException(DomainException):
    """Raised when domain entity validation fails."""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message)


class ResourceNotFoundException(DomainException):
    """Raised when a requested domain entity does not exist."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class ConflictException(DomainException):
    """Raised when an operation conflicts with the current domain state."""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message)


class AuthorizationException(DomainException):
    """Raised when a user is not authorized to perform an action on a domain entity."""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message)


class TenantIsolationException(DomainException):
    """Raised when an operation attempts to cross tenant boundaries."""
    def __init__(self, message: str = "Tenant isolation violation"):
        super().__init__(message)


class StateTransitionException(DomainException):
    """Raised when an invalid state transition is attempted on a domain entity."""
    def __init__(self, message: str = "Invalid state transition"):
        super().__init__(message)


class BusinessRuleViolation(DomainException):
    """Raised when a specific business rule is violated."""
    def __init__(self, message: str = "Business rule violation"):
        super().__init__(message)


# ─── Exception Handlers ───────────────────────────────────────────────────────

def setup_exception_handlers(app: FastAPI) -> None:
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    "request_id": request_id
                }
            },
        )
        
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": 422,
                    "message": "Validation Error",
                    "details": exc.errors(),
                    "request_id": request_id
                }
            },
        )
        
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.error(f"Unhandled exception: {exc} [request_id={request_id}]", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": 500,
                    "message": "Internal Server Error",
                    "request_id": request_id
                }
            },
        )
