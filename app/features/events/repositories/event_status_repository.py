from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.codable_repository import CodableRepository
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.exceptions.event_status_exceptions import DefaultEventStatusNotFoundError, \
    EventStatusNotFoundError
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

    async def get_published(self) -> EventStatus:
        stmt = (
            select(EventStatus)
            .where(EventStatus.code == EventStatusCode.PUBLISHED)
        )

        event_status = await self._session.scalar(stmt)

        if event_status is None:
            raise EventStatusNotFoundError(EventStatusCode.PUBLISHED)

        return event_status

    async def get_cancelled(self) -> EventStatus:
        stmt = (select(EventStatus).where(EventStatus.code == EventStatusCode.CANCELLED))

        event_status = await self._session.scalar(stmt)

        if event_status is None:
            raise EventStatusNotFoundError(EventStatusCode.CANCELLED)

        return event_status

    async def get_complete(self):
        stmt = (
            select(EventStatus).where(EventStatus.code == EventStatusCode.COMPLETED)
        )

        event_status = await self._session.scalar(stmt)

        if event_status is None:
            raise EventStatusNotFoundError(EventStatusCode.COMPLETED)

        return event_status