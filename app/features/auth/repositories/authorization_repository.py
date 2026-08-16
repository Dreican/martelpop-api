from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.exceptions.authorization_exceptions import RolePermissionNotFoundError
from app.features.auth.models.permission import Permission
from app.features.auth.models.role import Role
from app.features.auth.models.role_permission import RolePermission


class AuthorizationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=RolePermission, not_found_exception=RolePermissionNotFoundError)

    async def get_permission_codes(self, role_code: RoleCode) -> set[PermissionCode]:
        stmt = (select(Permission.code)
                .join(RolePermission)
                .join(Role)
                .where(Role.code == role_code))

        return set(await self._session.scalars(stmt))

    async def role_has_permission(self, role: Role, permission: PermissionCode) -> bool:
        stmt = (
            select(
                exists()
                .where(RolePermission.role_id == role.id)
                .where(RolePermission.permission_id == Permission.id)
                .where(Permission.code == permission)
            )
        )

        return await self._session.scalar(stmt) is not None
