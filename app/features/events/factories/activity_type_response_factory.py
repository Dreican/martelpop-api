from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.responses.activity_type_response import ActivityTypeResponse
from app.features.events.models.activity_type import ActivityType


class ActivityTypeResponseFactory(ResponseFactory[ActivityType, ActivityTypeResponse]):
    def __init__(self):
        super().__init__()

    def create(self, entity: ActivityType) -> ActivityTypeResponse:
        response = ActivityTypeResponse.model_validate(entity)

        response.icon_url = self.file_url(entity.banner_file_id)

        return response
