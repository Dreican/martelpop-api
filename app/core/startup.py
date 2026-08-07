from contextlib import asynccontextmanager

from fastapi import FastAPI

import logging
from app.core.database.seeders.runnner import seed_database
from app.features.auth.services.authentication_service import AuthenticationService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")

    await seed_database()
    logger.info("Database seeded")

    app.state.authentication = AuthenticationService()
    app.state.settings = get_settings()

    yield

    logger.info("Stopping application")
