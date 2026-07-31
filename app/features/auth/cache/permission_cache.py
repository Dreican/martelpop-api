import logging

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.repositories.authorization_repository import AuthorizationRepository

logger = logging.getLogger(__name__)

class PermissionCache:
    def __init__(self,authorization_repository: AuthorizationRepository):
        self._authorization = authorization_repository
        self._cache: dict[RoleCode, frozenset[PermissionCode]] = {}

    def get(self, role: RoleCode) -> frozenset[PermissionCode] | None:
        return self._cache.get(role)

    def add(self, role: RoleCode, permissions: frozenset[PermissionCode]) -> None:
        self._cache[role] = permissions

    def invalidate(self, role: RoleCode) -> None:
        self._cache.pop(role, None)

    def clear(self) -> None:
        self._cache.clear()

    async def get_permissions(self, role: RoleCode) -> frozenset[PermissionCode]:
        permissions = self._cache.get(role)

        if permissions is not None:
            logger.debug("Permission cache hit for role %s", role.value)
            return permissions

        logger.debug("Permission cache miss for role %s",role.value)

        permissions = frozenset(
            await self._authorization.get_permission_codes(role)
        )

        self._cache[role] = permissions

        return permissions

