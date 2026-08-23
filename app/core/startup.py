import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database.seeders.runnner import seed_database
from app.features.auth.services.password_service import PasswordService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")

    password_service = PasswordService()
    await seed_database(password_service)
    logger.info("Database seeded")

    yield

    logger.info("Stopping application")
