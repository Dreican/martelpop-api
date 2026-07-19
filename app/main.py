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
async def lifespan(app: FastAPI):
    logger.info("Starting application")

    await seed_database()

    yield

    logger.info("Stopping application")


app = FastAPI(
    lifespan=lifespan
)
app.include_router(api_router)

configure_cors(app)
logger.info("CORS configured")

configure_trusted_hosts(app)
logger.info("Trusted hosts configured")

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestContextMiddleware)
logger.info("Request logging middleware configured")

register_exception_handlers(app)
logger.info("Exception handlers registered")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

logger.info(f"Application started : http://{get_settings().app.host}:{get_settings().app.port}")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
