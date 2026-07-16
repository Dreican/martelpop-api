import logging

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.logging_config import setup_logging
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
app = FastAPI()

logger = logging.getLogger(__name__)
logger.info("Starting the application")

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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
