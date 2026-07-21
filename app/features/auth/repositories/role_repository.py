from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.auth.models.role import Role


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Role)

    async def get_by_id(self, role_id: UUID) -> Role | None:
        stmt = (select(Role).where(Role.id == role_id))
        return await self._session.scalar(stmt)

    async def get_by_name(self, role_name: str) -> Role | None:
        stmt = (select(Role).where(Role.name == role_name))
        return await self._session.scalar(stmt)

    async def get_all(self) -> list[Role]:
        stmt = select(Role)

        return list(await self._session.scalars(stmt))

    async def get_default_role(self) -> Role | None:
        stmt = (select(Role).where(Role.is_default == True))
        return await self._session.scalar(stmt)

