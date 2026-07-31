import logging

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.security.principal import Principal

logger = logging.getLogger(__name__)


class AuthorizationService:

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

    @staticmethod
    def has_permission(principal: Principal, permission: PermissionCode) -> bool:
        return permission in principal.permissions

    @staticmethod
    def has_any_permissions(principal: Principal, permissions: set[PermissionCode]) -> bool:
        return bool(principal.permissions & permissions)

    @staticmethod
    def has_all_permissions(principal: Principal, permissions: set[PermissionCode]) -> bool:
        return permissions.issubset(principal.permissions)
