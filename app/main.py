import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.core.database.models
from app.api.v1.router import api_router
from app.core.config.settings import get_settings
from app.core.database.seeders.runnner import seed_database
from app.core.logging.config import setup_logging
from app.middleware import (
    configure_cors,
    configure_trusted_hosts,
    RequestContextMiddleware,
    RequestLoggingMiddleware,
)
from app.middleware.error_handling import (
    register_exception_handlers,
)

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(api: FastAPI):
    logger.info("Starting application")

    await seed_database()

    yield

    logger.info("Stopping application")


api = FastAPI(
    lifespan=lifespan
)
api.include_router(api_router)

configure_cors(api)
logger.info("CORS configured")

configure_trusted_hosts(api)
logger.info("Trusted hosts configured")

api.add_middleware(RequestLoggingMiddleware)
api.add_middleware(RequestContextMiddleware)
logger.info("Request logging middleware configured")

register_exception_handlers(api)
logger.info("Exception handlers registered")

api.mount("/static", StaticFiles(directory="app/static"), name="static")

logger.info(f"Application started : http://localhost:{get_settings().app.port}")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")

