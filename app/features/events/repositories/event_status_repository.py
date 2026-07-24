from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.core.database.repositories.codable_repository import CodableRepository
from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.exceptions.event_status_exceptions import DefaultEventStatusNotFoundError
from app.features.events.models.event_status import EventStatus


class EventStatusRepository(CodableRepository[EventStatus, EventStatusCode]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=EventStatus, not_found_exception=DefaultEventStatusNotFoundError)

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

    async def get_default(self) -> EventStatus:
        stmt = (
            select(EventStatus)
                .where(EventStatus.is_default == True)
        )

        event_status = await self._session.scalar(stmt)

        if event_status is None:
            raise DefaultEventStatusNotFoundError()

        return event_status
