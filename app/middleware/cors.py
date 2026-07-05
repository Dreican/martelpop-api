from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:80",
            "http://localhost:8080",
            "http://localhost:443",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )