from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.slug import SlugServiceDep
from app.core.pagination.page import Page
from app.core.services.base_service import BaseService
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_search_request import UserSearchRequest
from app.features.users.factories.user_response_factory import UserResponseFactory
from app.features.users.repositories.user_repository import UserRepository


class UserService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            slug_service: SlugServiceDep,
            user_response: UserResponseFactory
    ):
        super().__init__(session)
        self._users = user_repository
        self._roles = role_repository
        self._slug = slug_service
        self._user_response = user_response


    async def search(self, request: UserSearchRequest, principal: AuthenticatedPrincipal) -> Page[UserResponse]:
        if not principal.is_admin:
            raise PermissionDeniedError(permissions={PermissionCode.USER_READ}, user=principal.user.display_name)

        return self._user_response.create_page(await self._users.search(request))

    async def update(self, request: UserUpdateRequest, principal: AuthenticatedPrincipal) -> UserResponse: