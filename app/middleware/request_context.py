import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request.state.started_id = str(uuid.uuid4())
        request.state.started_at = time.perf_counter()

        request.state.client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        request.state.user = None

        response = await call_next(request)

        response.headers["X-Request-Id"] = request.state.started_id

        return response
