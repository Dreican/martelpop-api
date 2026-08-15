from fastapi import APIRouter

from app.api.v1.routes.admin import events, users

api_admin_router = APIRouter(prefix="/admin")

api_admin_router.include_router(events.router)
api_admin_router.include_router(users.router)
