import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.status import (
    HTTP_422_UNPROCESSABLE_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from app.core.constants import ErrorCode
from app.core.exceptions.base import ApplicationError
from app.core.exceptions.errors import ErrorResponse, FieldError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        logger.warning(
            "%s %s -> %s (%s)",
            request.method,
            request.url.path,
            exc.code,
            exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=exc.code,
                detail=exc.detail
            ).model_dump(mode="json"),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        validation_errors: list[FieldError] = []

        for error in exc.errors():
            loc = error.get("loc", ())
            if loc and loc[0] in {"body", "query", "path", "header", "cookie"}:
                loc = loc[1:]

            field = ".".join(map(str, loc)) or "request"

            validation_errors.append(
                FieldError(
                    field=field,
                    message=error["msg"],
                )
            )

        logger.info(
            "Request validation failed: %s %s -> %s",
            request.method,
            request.url.path,
            [
                f"{e.field}: {e.message}"
                for e in validation_errors
            ],
        )

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
            content=ErrorResponse(
                code=ErrorCode.VALIDATION_ERROR,
                detail="Request validation failed",
                errors=validation_errors,
            ).model_dump(mode="json"),
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
        logger.exception("Internal validation error")

        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                code=ErrorCode.INTERNAL_VALIDATION_ERROR,
                detail="Internal validation error"
            ).model_dump(mode="json"),
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
            request: Request,
            exc: Exception,
    ) -> JSONResponse:
        logger.exception(
            "Unhandled exception during %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            ).model_dump(mode="json"),
        )
