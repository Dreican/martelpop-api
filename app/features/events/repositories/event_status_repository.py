from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.models.event_status import EventStatus



class EventStatusRepository(SluggableRepository[EventStatusCode]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=EventStatusCode)

    async def get_by_code(self, code: EventStatusCode) -> EventStatus | None:
        stmt = (
            select(EventStatus)
                .where(EventStatus.code == code)
        )
        return await self._session.scalar(stmt)

    async def get_all(self) -> list[EventStatus]:
        stmt = (
            select(EventStatus)
        )
        return list(await self._session.scalars(stmt))

    async def get_all_codes(self) -> list[EventStatusCode]:
        stmt = (
            select(EventStatus.code)
        )
        return list(await self._session.scalars(stmt))

