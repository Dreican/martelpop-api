from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.activity_type_response import ActivityTypeResponse
from app.features.events.models.event import Event
from app.features.storage.services.sotrage_service import StorageService


class ActivityTypeResponseFactory(ResponseFactory[Event, ActivityTypeResponse]):
    def __init__(self, storage: StorageService):
        super().__init__(storage)

    def create(self, entity: Event) -> ActivityTypeResponse:
        response = ActivityTypeResponse.model_validate(entity)

        response.icon_url = self._storage.public_url(entity.banner_file_id)

        return response