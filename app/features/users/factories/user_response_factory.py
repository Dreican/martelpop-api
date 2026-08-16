from app.core.factories.response_factory import ResponseFactory
from app.features.auth.factories.role_summary_response_factory import RoleSummaryResponseFactory
from app.features.storage.services.sotrage_service import StorageService
from app.features.users.dto.user_response import UserResponse
from app.features.users.models.user import User


class UserResponseFactory(ResponseFactory[User, UserResponse]):
    def __init__(self, storage: StorageService, role: RoleSummaryResponseFactory):
        super().__init__(storage)
        self._role = role

    def create(self, entity: User) -> UserResponse:
        response = UserResponse.model_validate(entity)

        response.avatar_url = self._storage.public_url(entity.avatar_file_id)
        response.role = self._role.create(entity.role)

        return response
