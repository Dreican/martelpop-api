import logging
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.features.events.enums.event_status import EventStatus
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event

logger = logging.getLogger(__name__)


class EventRepository(SluggableRepository[Event]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Event)

    async def get_by_id(self, event_id: UUID) -> Event | None:
        stmt = (
            select(Event)
            .options(selectinload(ActivityType.events))
            .where(ActivityType.id == event_id)
        )
        return await self._session.scalar(stmt)

    async def get_by_activity_type(self, activity_type: ActivityType) -> Event | None:
        stmt = (
            select(Event).where(Event.activity_type == activity_type)
        )

        return await self._session.scalar(stmt)

    async def get_upcoming(self) -> list[Event]:
        stmt = (
            select(Event).where(
                Event.start_at > datetime.now(UTC),
                Event.status == EventStatus.PUBLISHED
            )
        )

        return list(await self._session.scalars(stmt))

    async def search(self, query: str) -> list[Event]:
        stmt = (
            select(Event)
            .where(Event.title.contains(query))
            .where(Event.description.contains(query))
        )

        return list(await self._session.scalars(stmt))
