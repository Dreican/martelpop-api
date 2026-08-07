from fastapi import APIRouter

from app.api.v1.routes.admin import events

api_admin_router = APIRouter(prefix="/admin")

api_admin_router.include_router(events.router)
