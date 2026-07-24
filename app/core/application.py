from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

import logging
from app.api.v1.router import api_router
from app.middleware import configure_cors, configure_trusted_hosts, RequestLoggingMiddleware, RequestContextMiddleware
from app.middleware.error_handling import register_exception_handlers

logger = logging.getLogger(__name__)


def configure_application(app: FastAPI):
    configure_cors(app)
    configure_trusted_hosts(app)

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestContextMiddleware)

    register_exception_handlers(app)

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(api_router)
