from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.features.auth.dependencies.current_user import CurrentUser
from app.features.auth.dependencies.permissions import permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.events.dependencies.services import EventServiceDep
from app.features.events.dto.event_create_request import EventCreateRequest
from app.features.events.dto.event_response import EventResponse
from app.features.events.dto.event_update_request import EventUpdateRequest

router = APIRouter(prefix="/events", tags=["Admin Events"])

@router.get("/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def get_events(event_id: UUID, _: permission(PermissionCode.EVENT_READ) , event_service: EventServiceDep, user: CurrentUser):
    return await event_service.get_event(event_id, user)

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreateRequest, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.create_event(event, user)

@router.patch("/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def update_event(event_id: UUID, event: EventUpdateRequest, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.update_event(event_id, event, user)

@router.delete("/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def delete_event(event_id: UUID, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.delete_event(event_id, user)

@router.post("/{event_id}/publish", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def publish_event(event_id: UUID, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.publish_event(event_id, user)

@router.post("/{event_id}/unpublish", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def unpublish_event(event_id: UUID, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.unpublish_event(event_id, user)

@router.post("/{event_id}/publish", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def publish_event(event_id: UUID, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.publish_event(event_id, user)

@router.post("/{event_id}/cancel", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def cancel_event(event_id: UUID, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.cancel_event(event_id, user)

@router.post("/{event_id}/complete", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def cancel_event(event_id: UUID, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.complete_event(event_id, user)