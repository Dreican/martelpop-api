from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.slug import SlugServiceDep
from app.features.users.repositories.user_repository import UserRepository


class UserService:
    def __init__(
            self,
            session: AsyncSession,
            user_repository: UserRepository,
            slug_service: SlugServiceDep
    ):
        self._session = session
        self._users = user_repository
        self._slug = slug_service
