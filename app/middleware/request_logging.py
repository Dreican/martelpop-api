import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        response = None

        try:
            response = await call_next(request)
            return response
        finally:
            duration = (time.perf_counter() - request.state.started_at) * 1000

            user = getattr(request.state, "user", None)

            user_id = (
                user.id
                if user is not None
                else "anonymous"
            )

            status = (
                response.status_code
                if response
                else 500
            )

            log = (
                f"[{request.state.request_id}] "
                f"{request.method} "
                f"{request.url.path} "
                f"status={status} "
                f"user={user_id} "
                f"ip={request.state.client_ip} "
                f"duration={duration:.2f}ms"
            )

            if status >= 500:
                logger.error(log)
            elif status >= 400:
                logger.warning(log)
            else:
                logger.info(log)
