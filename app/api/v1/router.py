from fastapi import APIRouter, Depends

from app.api.v1.admin_router import api_admin_router
from app.api.v1.auth_router import auth_router
from app.api.v1.routes import static, events
from app.features.auth.dependencies.maintenance import require_not_in_maintenance

api_router = APIRouter(prefix="/api/v1")

protected_api_router = APIRouter(
    dependencies=[Depends(require_not_in_maintenance)]
)

api_router.include_router(auth_router)
api_router.include_router(static.router)

protected_api_router.include_router(events.router)
protected_api_router.include_router(api_admin_router)

api_router.include_router(protected_api_router)
