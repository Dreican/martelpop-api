from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.responses.activity_type_summary_response import ActivityTypeSummaryResponse
from app.features.events.models.activity_type import ActivityType
from app.features.storage.services.sotrage_service import StorageService


class ActivityTypeSummaryResponseFactory(ResponseFactory[ActivityType, ActivityTypeSummaryResponse]):
    def __init__(self, storage: StorageService):
        super().__init__(storage)

    def create(self, entity: ActivityType) -> ActivityTypeSummaryResponse:
        response = ActivityTypeSummaryResponse.model_validate(entity)

        response.icon_url = self._storage.public_url(entity.banner_file_id)

        return response
