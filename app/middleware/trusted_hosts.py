from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware


def configure_trusted_hosts(app: FastAPI):
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "*.martelpop.local",
        ],
    )
