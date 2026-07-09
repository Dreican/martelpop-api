from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository[T]:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, entity: T) -> None:
        self._session.add(entity)

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, entity: T) -> None:
        await self._session.refresh(entity)