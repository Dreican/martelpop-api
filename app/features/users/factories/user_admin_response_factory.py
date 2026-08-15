from app.core.factories.response_factory import ResponseFactory
from app.features.storage.services.sotrage_service import StorageService
from app.features.users.dto.user_admin_response import UserAdminResponse
from app.features.users.models.user import User


class UserAdminResponseFactory(ResponseFactory[User, UserAdminResponse]):
    def __init__(self, storage: StorageService):
        super().__init__(storage)

    def create(self, entity: User) -> UserAdminResponse:
        response = UserAdminResponse.model_validate(entity)

        response.avatar_url = self._storage.public_url(entity.avatar_file_id)

        return response
