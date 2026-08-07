import logging

from fastapi import FastAPI

from app.core.application import configure_application
from app.core.logger.config import setup_logging
from app.core.startup import lifespan

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    lifespan=lifespan
)

configure_application(app)
