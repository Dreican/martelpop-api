from uuid import UUID

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.models.permission import Permission
from app.features.auth.models.role import Role
from app.features.auth.models.role_permission import RolePermission


class AuthorizationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_permission_codes(self, role: Role) -> set[PermissionCode]:
        stmt = (select(Permission.code)
                .join(RolePermission)
                .where(RolePermission.role_id == role.id))

        return set(await self._session.scalars(stmt))

    async def role_has_permission(self, role: Role, permission: PermissionCode) -> bool:
        stmt = (
            select(exists())
            .join(RolePermission)
            .where(RolePermission.role_id == role.id)
            .where(Permission.code == permission)
        )

        return await self._session.scalar(stmt) is not None