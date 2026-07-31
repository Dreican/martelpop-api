from fastapi import APIRouter, status, Depends

from app.core.pagination.page import Page
from app.features.auth.dependencies.current_principal import CurrentPrincipal
from app.features.auth.dependencies.current_user import CurrentUser
from app.features.auth.dependencies.permissions import permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.events.dependencies.services import EventServiceDep
from app.features.events.dto.event_response import EventResponse
from app.features.events.dto.event_search_request import EventSearchRequest

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

@router.get("/{event_slug}", response_model=EventResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(permission(PermissionCode.EVENT_READ))])
async def get_event(event_slug: str, event_service: EventServiceDep, principal: CurrentPrincipal):
    return await event_service.get_event_by_slug(event_slug, principal)

@router.get("/search", response_model=Page[EventResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(permission(PermissionCode.EVENT_READ))])
async def search_events(request: EventSearchRequest ,event_service: EventServiceDep, principal: CurrentPrincipal):
    return await event_service.list_events(request, principal)
