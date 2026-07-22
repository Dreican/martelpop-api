import logging

from fastapi import FastAPI

import app.core.database.models as _models
from app.api.v1.router import api_router
from app.core.application import configure_application
from app.core.logger.config import setup_logging
from app.core.startup import lifespan

__all__ = ["_models"]

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    lifespan=lifespan
)

configure_application(app)
app.include_router(api_router)
