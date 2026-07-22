import logging

from fastapi import FastAPI

from app.middleware import configure_cors, configure_trusted_hosts, RequestLoggingMiddleware, RequestContextMiddleware
from app.middleware.error_handling import register_exception_handlers

logger = logging.getLogger(__name__)


def configure_application(app: FastAPI):
    configure_cors(app)
    configure_trusted_hosts(app)

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestContextMiddleware)

    register_exception_handlers(app)
