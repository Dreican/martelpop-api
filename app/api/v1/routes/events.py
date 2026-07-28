from uuid import UUID

from fastapi import APIRouter, status

from app.core.dependencies.database import SessionDep
from app.core.pagination.page import Page
from app.features.auth.dependencies.current_user import CurrentUser
from app.features.events.dependencies.services import EventServiceDep
from app.features.events.dto.event_create_request import EventCreateRequest
from app.features.events.dto.event_response import EventResponse
from app.features.events.dto.event_search_request import EventSearchRequest
from app.features.events.dto.event_update_request import EventUpdateRequest

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

@router.get("/{event_slug}", response_model=EventResponse, status_code=status.HTTP_200_OK)
async def get_event(event_slug: str, event_service: EventServiceDep, user: CurrentUser):
    return await event_service.get_event_by_slug(event_slug, user)

@router.get("/search", response_model=Page[EventResponse], status_code=status.HTTP_200_OK)
async def search_events(request: EventSearchRequest ,event_service: EventServiceDep, user: CurrentUser):
    return await event_service.list_events(request, user)
