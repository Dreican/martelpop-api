from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _commit(self) -> None:
        await self._session.commit()

    async def _rollback(self) -> None:
        await self._session.rollback()

    async def _flush(self) -> None:
        await self._session.flush()

    async def _refresh(self, entity: T) -> T:
        await self._session.refresh(entity)
        return entity

    async def _save(self, entity: T) -> T:
        await self._flush()
        return await self._refresh(entity)
