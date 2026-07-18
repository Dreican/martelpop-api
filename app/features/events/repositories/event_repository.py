import logging
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select

from app.features.events.constants import EventStatus
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event
from app.shared.database.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class EventRepository(BaseRepository[Event]):

    async def get_by_id(self, event_id: UUID) -> Event | None:
        stmt = (
            select(Event).where(Event.id == event_id)
        )

        return await self._session.scalar(stmt)

    async def get_by_slug(self, slug: str) -> Event | None:
        stmt = (
            select(Event).where(Event.slug == slug)
        )

        return await self._session.scalar(stmt)

    async def slug_exist(self, slug: str) -> bool:
        stmt = (
            select(Event).where(Event.slug == slug)
        )

        return await self._session.scalar(stmt) is not None

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
            select(Event).where(
                Event.title.contains(query)
            )
        )

        return list(await self._session.scalars(stmt))
