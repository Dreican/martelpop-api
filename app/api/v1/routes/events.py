from fastapi import APIRouter, status

from app.core.pagination.page import Page
from app.features.auth.dependencies.require_permissions import permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import Principal
from app.features.events.dependencies.services import EventServiceDep
from app.features.events.dto.event_response import EventResponse
from app.features.events.dto.event_search_request import EventSearchRequest

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/search", response_model=Page[EventResponse], status_code=status.HTTP_200_OK)
async def search_events(request: EventSearchRequest, event_service: EventServiceDep, principal: Principal = permission(PermissionCode.EVENT_READ)):
    return await event_service.list_events(request, principal)

@router.get("/{event_slug}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def get_event(event_slug: str, event_service: EventServiceDep, principal: Principal = permission(PermissionCode.EVENT_READ)):
    return await event_service.get_event_by_slug(event_slug, principal)
