from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.config import Settings


def configure_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[Settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
