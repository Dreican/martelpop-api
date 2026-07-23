from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.settings import get_settings


def configure_cors(app: FastAPI):
    settings = get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors.allowed_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
