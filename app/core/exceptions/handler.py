import logging
from datetime import datetime, UTC

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.base import ApplicationError
from app.core.exceptions.errors import ErrorResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:

        logger.warning(
            "%s %s -> %s",
            request.method,
            request.url.path,
            exc.code,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=exc.code,
                detail=exc.detail,
                timestamp=datetime.now(UTC),
            ).model_dump(mode="json"),
        )