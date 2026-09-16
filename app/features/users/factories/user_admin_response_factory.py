from app.core.factories.response_factory import ResponseFactory
from app.features.auth.factories.role_summary_response_factory import RoleSummaryResponseFactory
from app.features.users.dto.user_admin_response import UserAdminResponse
from app.features.users.factories.user_summary_response_factory import UserSummaryResponseFactory
from app.features.users.models.user import User


class UserAdminResponseFactory(ResponseFactory[User, UserAdminResponse]):
    def __init__(self, role: RoleSummaryResponseFactory, user_summary: UserSummaryResponseFactory):
        super().__init__()
        self._role = role
        self._user_summary = user_summary

    def create(self, entity: User) -> UserAdminResponse:
        response = UserAdminResponse.model_validate(entity)

        response.avatar_url = self.file_url(entity.avatar_file_id)
        response.role = self._role.create(entity.role)
        response.deleted_by = self._user_summary.create(entity.deleted_by) if entity.deleted_by else None

        return response
