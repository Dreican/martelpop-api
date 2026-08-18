from app.core.factories.response_factory import ResponseFactory
from app.features.users.dto.user_summary_response import UserSummaryResponse
from app.features.users.models.user import User


class UserSummaryResponseFactory(ResponseFactory[User, UserSummaryResponse]):
    def __init__(self):
        super().__init__()

    def create(self, entity: User) -> UserSummaryResponse:
        response = UserSummaryResponse.model_validate(entity)

        response.avatar_url = self.file_url(entity.avatar_file_id)

        return response
