from uuid import UUID

from fastapi import APIRouter, status

from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.dependencies.services import EventServiceDep
from app.features.events.dto.requests.event_create_request import EventCreateRequest
from app.features.events.dto.responses.event_response import EventResponse
from app.features.events.dto.requests.event_update_request import EventUpdateRequest

router = APIRouter(prefix="/events", tags=["Admin Events"])

@router.get("/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def get_events(event_id: UUID, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_READ)):
    return await event_service.get_event(event_id, principal)

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreateRequest, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_CREATE)):
    return await event_service.create_event(event, principal)

@router.patch("/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def update_event(event_id: UUID, event: EventUpdateRequest, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_UPDATE)):
    return await event_service.update_event(event_id, event, principal)

@router.delete("/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def delete_event(event_id: UUID, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_DELETE)):
    return await event_service.delete_event(event_id, principal)

@router.post("/{event_id}/publish", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def publish_event(event_id: UUID, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_PUBLISH)):
    return await event_service.publish_event(event_id, principal)

@router.post("/{event_id}/unpublish", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def unpublish_event(event_id: UUID, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_PUBLISH)):
    return await event_service.unpublish_event(event_id, principal)

@router.post("/{event_id}/cancel", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def cancel_event(event_id: UUID, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_CANCEL)):
    return await event_service.cancel_event(event_id, principal)

@router.post("/{event_id}/complete", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def complete_event(event_id: UUID, event_service: EventServiceDep, principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.EVENT_PUBLISH)):
    return await event_service.complete_event(event_id, principal)