import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.repositories.authorization_repository import AuthorizationRepository
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.users.models.user import User


logger = logging.getLogger(__name__)

class AuthorizationService:
    def __init__(
            self,
            authorization_repository: AuthorizationRepository,
    ):
        self._authorization = authorization_repository


    async def has_permission(self, user: User, permission: PermissionCode) -> bool:
        permissions = await self._authorization.get_permission_codes(user.role)
        logger.debug(f"Checking if user {user.email} has permissions {permission.value}")
        return permission in permissions

    async def require_permission(self, user: User, permission: PermissionCode) -> None:
        if not await self.has_permission(user, permission):
            logger.error(f"User {user.email} does not have permission {permission.value}")
            raise PermissionDeniedError(f"User {user.email} does not have permission {permission.value}")

        logger.debug(f"User {user.email} has permission {permission.value}")

    async def has_any_permissions(self, user: User, permissions: list[PermissionCode]) -> bool:
        user_permissions = await self._authorization.get_permission_codes(user.role)
        logger.debug(f"Checking if user {user.email} has any permissions {permissions}")
        return any(permission in user_permissions for permission in permissions)

    async def has_all_permissions(self, user: User, permissions: list[PermissionCode]) -> bool:
        user_permissions = await self._authorization.get_permission_codes(user.role)
        logger.debug(f"Checking if user {user.email} has all permissions {permissions}")
        return all(permission in user_permissions for permission in permissions)
