from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.configuration import get_config


def configure_cors(app: FastAPI):
    settings = get_config()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
