from app.core.factories.response_factory import ResponseFactory
from app.features.events.dto.responses.activity_type_admin_response import ActivityTypeAdminResponse
from app.features.events.models.activity_type import ActivityType
from app.features.users.dto.user_summary_response import UserSummaryResponse
from app.features.users.factories.user_summary_response_factory import UserSummaryResponseFactory


class ActivityTypeAdminResponseFactory(ResponseFactory[ActivityType, ActivityTypeAdminResponse]):
    def __init__(self, user: UserSummaryResponseFactory):
        super().__init__()
        self.user_response = user

    def create(self, entity: ActivityType) -> ActivityTypeAdminResponse:
        response = ActivityTypeAdminResponse.model_validate(entity)

        response.icon_url = self.file_url(entity.icon_file_id)
        response.banner_url = self.file_url(entity.banner_file_id)
        if entity.deleted_by is not None:
            response.deleted_by = self.user_response.create(entity.deleted_by)

        return response
