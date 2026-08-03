from app.core.factories.response_factory import ResponseFactory
from app.features.storage.services.sotrage_service import StorageService
from app.features.users.dto.user_response import UserResponse
from app.features.users.models.user import User


class UserResponseFactory(ResponseFactory[User, UserResponse]):
    def __init__(self, storage: StorageService):
        self._storage = storage


    def create(self, entity: User) -> UserResponse:
        response: UserResponse = super().create(entity)

        response.avatar_url = self._storage.public_url(entity.avatar_file_id)

        return response