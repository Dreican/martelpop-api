from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.event_response import EventResponse
from app.features.events.models.event import Event
from app.features.storage.services.sotrage_service import StorageService


class EventResponseFactory(ResponseFactory[Event, EventResponse]):
    def __init__(self, storage: StorageService):
        self._storage = storage


    def create(self, entity: Event) -> EventResponse:
        response: EventResponse = super().create(entity)

        response.banner_url = self._storage.public_url(entity.banner_file_id)
        response.activity_type.icon_url = self._storage.public_url(entity.activity_type.icon_file_id)
        response.creator.avatar_url = self._storage.public_url(entity.creator.avatar_file_id)

        return response