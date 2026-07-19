from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.auth.models.role import Role


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(self, role_id: UUID) -> Role | None:
        stmt = (select(Role).where(Role.id == role_id))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, role_name: str) -> Role | None:
        stmt = (select(Role).where(Role.name == role_name))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_default_role(self) -> Role | None:
        stmt = (select(Role).where(Role.is_default == True))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
