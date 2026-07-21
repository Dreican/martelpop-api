import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.repositories.authorization_repository import AuthorizationRepository
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.users.models.user import User


logger = logging.getLogger(__name__)

class AuthorizationService:
    def __init__(
            self,
            session: AsyncSession,
            role_repository: RoleRepository,
            permissions_repository: AuthorizationRepository,
    ):
        self._session = session
        self._roles = role_repository
        self._permissions = permissions_repository

    async def has_permission(self, user: User, permission: PermissionCode) -> bool:
        permissions = self._permissions.get_permission_codes(user.role)
        logger.debug(f"Checking if user {user.email} has permissions {permission.value}")
        return permission in permissions

    async def has_any_permissions(self, user: User, permissions: list[PermissionCode]) -> bool:
        user_permissions = self._permissions.get_permission_codes(user.role)
        logger.debug(f"Checking if user {user.email} has any permissions {permissions}")
        return any(permission in user_permissions for permission in permissions)

    async def has_all_permissions(self, user: User, permissions: list[PermissionCode]) -> bool:
        user_permissions = self._permissions.get_permission_codes(user.role)
        logger.debug(f"Checking if user {user.email} has all permissions {permissions}")
        return all(permission in user_permissions for permission in permissions)