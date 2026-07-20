from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository[T]:
    def __init__(self, session: AsyncSession, model: type[T]):
        self.model = model
        self._session = session

    async def add(self, entity: T) -> None:
        self._session.add(entity)

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, entity: T) -> None:
        await self._session.refresh(entity)

    async def get_by_id(self, entity_id: UUID) -> T | None:
        stmt = select(self.model).where(self.model.id == entity_id)
        return await self._session.scalar(stmt)
