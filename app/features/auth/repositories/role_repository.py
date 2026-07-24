import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.codable_repository import CodableRepository
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.exceptions.authentication_exceptions import RoleNotFoundError, DefaultRoleNotFoundError
from app.features.auth.models.role import Role

logger = logging.getLogger(__name__)


class RoleRepository(CodableRepository[Role, RoleCode]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Role, not_found_exception=RoleNotFoundError)

    async def get_by_name(self, role_name: str) -> Role | None:
        stmt = (select(Role).where(Role.name == role_name))
        return await self._session.scalar(stmt)

    async def get_all(self) -> list[Role]:
        stmt = select(Role)

        return list(await self._session.scalars(stmt))

    async def get_default_role(self) -> Role:
        stmt = (select(Role).where(Role.is_default == True))

        role = await self._session.scalar(stmt)
        if role is None:
            logger.error("Default role not found")
            raise DefaultRoleNotFoundError()

        return role
