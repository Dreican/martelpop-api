import logging

from app.features.auth.cache.permission_cache import PermissionCache
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.exceptions.helper import unauthorized
from app.features.auth.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.auth.services.jwt_service import JwtService
from app.features.users.models.user import User
from app.features.users.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class PrincipalService:

    def __init__(
            self,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            jwt_service: JwtService,
            permission_cache: PermissionCache,
    ) -> None:
        self._users = user_repository
        self._roles = role_repository
        self._jwt = jwt_service
        self._cache = permission_cache

    async def authenticate(self, access_token: str | None) -> Principal:
        user = await self._resolve_user(access_token)

        return await self._create_principal(user)

    @staticmethod
    def require_authenticated(principal: Principal) -> AuthenticatedPrincipal:
        if principal.user is None:
            unauthorized("Not authenticated.")

        return AuthenticatedPrincipal(
            user=principal.user,
            role=principal.role,
            permissions=principal.permissions,
        )

    async def _resolve_user(self, access_token: str | None) -> User | None:
        if access_token is None:
            return None

        try:
            payload = self._jwt.decode_access_token(access_token)
        except (ExpiredTokenError, InvalidTokenError):
            return None

        user = await self._users.required_for_authentication(payload.sub)

        if (
            not user.is_active
            or user.is_deleted
        ):
            return None

        return user

    async def _create_principal(self, user: User | None) -> Principal:
        if user is None:
            role = await self._roles.require_by_code(RoleCode.ANONYMOUS)
        else:
            role = user.role

        permissions = await self._cache.get_permissions(role.code)

        return Principal(
            user=user,
            role=role,
            permissions=frozenset(permissions),
        )
