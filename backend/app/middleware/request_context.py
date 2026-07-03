import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger

logger = get_logger("constructpulse.request")

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.perf_counter()
        
        try:
            response = await call_next(request)
            process_time = (time.perf_counter() - start_time) * 1000
            
            # Log successful request
            logger.info(
                f"method={request.method} path={request.url.path} "
                f"status={response.status_code} duration={process_time:.2f}ms "
                f"request_id={request_id}"
            )
            
            # Inject response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            
            return response
            
        except Exception as exc:
            process_time = (time.perf_counter() - start_time) * 1000
            # Log failed request
            logger.error(
                f"method={request.method} path={request.url.path} "
                f"status=500 duration={process_time:.2f}ms "
                f"request_id={request_id} error=\"{str(exc)}\""
            )
            raise
