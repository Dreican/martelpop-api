import logging

from app.features.auth.cache.permission_cache import PermissionCache
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.models.role import Role
from app.features.auth.repositories.authorization_repository import AuthorizationRepository
from app.features.users.models.user import User

logger = logging.getLogger(__name__)


class AuthorizationService:
    def __init__(
            self,
            authorization_repository: AuthorizationRepository,
            permission_cache: PermissionCache,
    ):
        self._authorization = authorization_repository
        self._cache = permission_cache

    async def has_permission(self, user: User, permission: PermissionCode) -> bool:
        permissions = await self._get_permission_codes(user.role)

        return permission in permissions

    async def require_permission(self, user: User, permission: PermissionCode) -> None:
        if not await self.has_permission(user, permission):
            logger.warning("Permission denied: user=%s permission=%s", user.email, permission.value)
            raise PermissionDeniedError(permission)

    async def require_all_permissions(self, user: User, permissions: set[PermissionCode]) -> None:
        if not await self.has_all_permissions(user, permissions):
            logger.warning("Permission denied: user=%s permissions=%s", user.email, permissions)
            raise PermissionDeniedError(permissions)

    async def require_any_permissions(self, user: User, permissions: set[PermissionCode]) -> None:
        if not await self.has_any_permissions(user, permissions):
            logger.warning("Permission denied: user=%s permissions=%s", user.email, permissions)
            raise PermissionDeniedError(permissions)

    async def has_any_permissions(self, user: User, permissions: set[PermissionCode]) -> bool:
        user_permissions = await self._get_permission_codes(user.role)
        return bool(user_permissions & permissions)

    async def has_all_permissions(self, user: User, permissions: set[PermissionCode]) -> bool:
        user_permissions = await self._get_permission_codes(user.role)
        return permissions.issubset(user_permissions)

    def invalidate_role(self, role: Role) -> None:
        self._cache.invalidate(role.code)

    async def _get_permission_codes(self, role: Role) -> set[PermissionCode]:
        permissions = self._cache.get(role.code)
        if permissions is not None:
            logger.debug("Permission cache hit for role %s", role.code.value)
            return permissions

        logger.debug("Permission cache miss for role %s", role.code.value)
        permissions = await self._authorization.get_permission_codes(role)
        self._cache.add(role.code, permissions)

        return permissions
