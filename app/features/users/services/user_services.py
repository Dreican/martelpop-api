from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.slug import SlugServiceDep
from app.core.services.base_service import BaseService
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.users.repositories.user_repository import UserRepository


class UserService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            slug_service: SlugServiceDep
    ):
        super().__init__(session)
        self._users = user_repository
        self._roles = role_repository
        self._slug = slug_service
