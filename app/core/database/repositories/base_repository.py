from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository[T]:
    def __init__(self, session: AsyncSession, model: type[T], not_found_exception: type[Exception]):
        self._model = model
        self._session = session
        self._not_found_exception = not_found_exception

    async def add(self, entity: T) -> None:
        self._session.add(entity)

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, entity: T) -> None:
        await self._session.refresh(entity)

    async def get_by_id(self, entity_id: UUID) -> T | None:
        stmt = select(self._model).where(self._model.id == entity_id)
        return await self._session.scalar(stmt)

    async def get_required(self, entity_id: UUID) -> T:
        entity  = await self.get_by_id(entity_id)

        if entity  is None:
            raise self._not_found_exception()

        return entity