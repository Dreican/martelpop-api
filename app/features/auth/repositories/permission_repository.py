from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.codable_repository import CodableRepository
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionNotFoundError
from app.features.auth.models.permission import Permission
from app.features.auth.models.role import Role
from app.features.auth.models.role_permission import RolePermission


class PermissionRepository(CodableRepository[Permission, PermissionCode]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Permission, not_found_exception=PermissionNotFoundError)

    async def get_all(self) -> list[Permission]:
        stmt = select(Permission)

        return list(await self._session.scalars(stmt))

    async def get_by_role(self, role: Role) -> list[Permission]:
        stmt = (
            select(Permission)
            .join(RolePermission)
            .where(RolePermission.role_id == role.id)
        )

        return list(await self._session.scalars(stmt))
