from uuid import UUID

from app.features.events.dto.event_response import EventResponse
from app.features.events.models.activity_type import ActivityType
from app.features.events.repositories.event_repository import EventRepository


class EventService:
    def __init__(
            self,
            event_repository: EventRepository
    ):
        self._event = event_repository


    async def get_event(self, event_id: UUID) -> EventResponse:
        return await self._event.get_by_id(event_id)

    async def get_event_by_activity_type(self, activity_type: ActivityType):
        return await self._event.get_by_activity_type(activity_type)