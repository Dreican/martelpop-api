import logging
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.enums.event_audience import EventAudience
from app.features.events.exceptions.event_exceptions import EventNotFoundError
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event
from app.features.users.models.user import User

logger = logging.getLogger(__name__)


class EventRepository(SluggableRepository[Event]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Event, not_found_exception=EventNotFoundError)

    async def get_by_id_with_activity(self, entity_id: UUID) -> Event | None:
        stmt = (
            select(Event)
            .options(selectinload(ActivityType.events))
            .where(ActivityType.id == entity_id)
        )
        return await self._session.scalar(stmt)

    async def get_by_activity_type(self, activity_type_id: UUID) -> list[Event]:
        stmt = (
            select(Event).where(Event.activity_type.id == activity_type_id)
        )

        return list(await self._session.scalars(stmt))

    async def get_upcoming(self) -> list[Event]:
        stmt = (
            select(Event).where(
                Event.start_at > datetime.now(UTC),
                Event.status == EventStatusCode.PUBLISHED
            )
        )

        return list(await self._session.scalars(stmt))

    async def get_all(self) -> list[Event]:
        stmt = (
            select(Event)
        )
        return list(await self._session.scalars(stmt))

    async def search(self, query: str) -> list[Event]:
        stmt = (
            select(Event)
            .where(
                or_(
                    Event.title.contains(query),
                    Event.description.contains(query)
                )
            )
        )

        return list(await self._session.scalars(stmt))

    async def get_audience_required(self, event_id: UUID, audience: EventAudience) -> Event | None:
        stmt = (
            select(Event)
            .where(Event.id == event_id)
            .where(Event.audience == audience)
        )

        return await self._session.scalar(stmt)