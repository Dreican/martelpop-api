import logging

from app.features.auth.cache.permission_cache import PermissionCache
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.models.role import Role
from app.features.auth.repositories.authorization_repository import AuthorizationRepository
from app.features.auth.security.principal import Principal
from app.features.users.models.user import User

logger = logging.getLogger(__name__)


class AuthorizationService:
    # def __init__(
    #         self,
    #         authorization_repository: AuthorizationRepository,
    #         permission_cache: PermissionCache,
    # ):
    #     self._authorization = authorization_repository
    #     self._cache = permission_cache

    async def require_permission(self, principal: Principal, permission: PermissionCode) -> None:
        if not self.has_permission(principal, permission):
            logger.warning("Permission denied: user=%s permission=%s", principal.fullname, permission.value)
            raise PermissionDeniedError({permission}, user=principal.fullname)

    async def require_all_permissions(self, principal: Principal, permissions: set[PermissionCode]) -> None:
        if not self.has_all_permissions(principal, permissions):
            logger.warning("Permission denied: user=%s permissions=%s", principal.fullname, permissions)
            raise PermissionDeniedError(permissions, user=principal.fullname)

    async def require_any_permissions(self, principal: Principal, permissions: set[PermissionCode]) -> None:
        if not self.has_any_permissions(principal, permissions):
            logger.warning("Permission denied: user=%s permissions=%s", principal.fullname, permissions)
            raise PermissionDeniedError(permissions, user=principal.fullname)

    def has_permission(self, principal: Principal, permission: PermissionCode) -> bool:
        return permission in principal.permissions

    def has_any_permissions(self, principal: Principal, permissions: set[PermissionCode]) -> bool:
        return bool(principal.permissions & permissions)

    def has_all_permissions(self, principal: Principal, permissions: set[PermissionCode]) -> bool:
        return permissions.issubset(principal.permissions)

    # def invalidate_role(self, role: Role) -> None:
    #     self._cache.invalidate(role.code)
    #
    # async def _get_permission_codes(self, role_code: RoleCode) -> set[PermissionCode]:
    #     permissions = self._cache.get(role_code)
    #     if permissions is not None:
    #         logger.debug("Permission cache hit for role %s", role_code.value)
    #         return permissions
    #
    #     logger.debug("Permission cache miss for role %s", role_code.value)
    #     permissions = await self._authorization.get_permission_codes(role_code)
    #     self._cache.add(role_code, permissions)
    #
    #     return permissions
