from fastapi import APIRouter

from app.api.v1.routes import auth

auth_router = APIRouter(
    prefix="/api/v1",
)

auth_router.include_router(auth.router)
