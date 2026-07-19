from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository[T]:
    def __init__(self, session: AsyncSession, model: type[T]):
        self._session = session
        self._model = model

    async def add(self, entity: T) -> None:
        self._session.add(entity)

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, entity: T) -> None:
        await self._session.refresh(entity)
