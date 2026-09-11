import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration = (time.perf_counter() - start) * 1000

            logger.exception(
                "[%s] %s %s status=500 duration=%.2fms",
                request.state.request_id,
                request.method,
                request.url.path,
                duration,
            )

            raise

        duration = (time.perf_counter() - start) * 1000
        status = getattr(response, "status_code", None)

        user = getattr(request.state, "user", None)
        user_display_name = getattr(user, "display_name", "anonymous")

        log = (
            f"[{request.state.request_id}] "
            f"{request.method} "
            f"{request.url.path} "
            f"status={status} "
            f"user={user_display_name} "
            f"ip={request.state.client_ip} "
            f"duration={duration:.2f}ms"
        )

        properties = {
            "log_props": {
                "RequestId": request.state.request_id,
                "RequestMethod": request.method,
                "RequestPath": request.url.path,
                "StatusCode": status,
                "UserDisplayName": str(user_display_name),
                "ClientIp": request.state.client_ip,
                "ElapsedMs": round(duration, 2),
            }
        }

        if status is not None and status >= 500:
            logger.error(log, extra=properties)
        elif status is not None and status >= 400:
            logger.warning(log, extra=properties)
        else:
            logger.info(log, extra=properties)

        return response
