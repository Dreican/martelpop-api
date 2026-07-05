import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppException(Exception):

    def __init__(
            self,
            message: str,
            status_code: int = 400,
    ):
        self.message = message
        self.status_code = status_code


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(
            request: Request,
            exc: AppException,
    ):
        logger.warning(
            "[%s] %s",
            request.state.request_id,
            exc.message,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.message,
                "request_id": request.state.request_id,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
            request: Request,
            exc: Exception,
    ):
        logger.exception(
            "[%s] Unexpected error",
            request.state.request_id,
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request.state.request_id,
            },
        )
