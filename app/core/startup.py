from contextlib import asynccontextmanager

from fastapi import FastAPI

import logging
from app.core.database.seeders.runnner import seed_database

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")

    await seed_database()
    logger.info("Database seeded")

    yield

    logger.info("Stopping application")
