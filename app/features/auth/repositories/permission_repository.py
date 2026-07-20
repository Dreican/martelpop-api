from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.models.permission import Permission


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Permission)
        self._session = session

    async def get_by_code(self, code: PermissionCode) -> Permission | None:
        return await self._session.get(Permission, code)