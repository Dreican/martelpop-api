from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.responses.activity_type_response import ActivityTypeResponse
from app.features.events.models.activity_type import ActivityType
from app.features.storage.services.sotrage_service import StorageService


class ActivityTypeResponseFactory(ResponseFactory[ActivityType, ActivityTypeResponse]):
    def __init__(self, storage: StorageService):
        super().__init__(storage)

    def create(self, entity: ActivityType) -> ActivityTypeResponse:
        response = ActivityTypeResponse.model_validate(entity)

        response.icon_url = self._storage.public_url(entity.banner_file_id)

        return response
