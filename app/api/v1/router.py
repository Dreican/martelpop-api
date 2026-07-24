from fastapi import APIRouter

from app.api.v1.routes import static, auth

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(static.router)
api_router.include_router(auth.router)
