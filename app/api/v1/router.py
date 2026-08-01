from fastapi import APIRouter

from app.api.v1.admin_router import api_admin_router
from app.api.v1.routes import static, auth, events

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(static.router)
api_router.include_router(auth.router)
api_router.include_router(events.router)

api_router.include_router(api_admin_router)
