from fastapi import APIRouter, status

from app.core.pagination.page import Page
from app.features.auth.dependencies.require_permissions import permission, authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.events.dependencies.services import EventServiceDep
from app.features.events.dto.requests.event_search_request import EventSearchRequest
from app.features.events.dto.responses.event_response import EventResponse
from app.features.registrations.dependencies.services import RegistrationServiceDep
from app.features.registrations.dto.requests.registration_create_request import RegistrationRequest
from app.features.registrations.dto.responses.registration_response import RegistrationResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/search", response_model=Page[EventResponse], status_code=status.HTTP_200_OK)
async def search_events(request: EventSearchRequest, event_service: EventServiceDep,
                        principal: Principal = permission(PermissionCode.EVENT_READ)):
    return await event_service.list_events(request, principal)


@router.get("/{event_slug}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def get_event(event_slug: str, event_service: EventServiceDep,
                    principal: Principal = permission(PermissionCode.EVENT_READ)):
    return await event_service.get_event_by_slug(event_slug, principal)


@router.post("/{event_slug}/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register(
        event_slug: str,
        request: RegistrationRequest,
        registration_service: RegistrationServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.REGISTRATION_CREATE)
):
    return await registration_service.register(event_slug, request, principal)


