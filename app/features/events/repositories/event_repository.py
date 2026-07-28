import logging
from datetime import datetime, UTC
from typing import Collection
from uuid import UUID

from sqlalchemy import select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.mixin.soft_delete import SoftDeleteMixin
from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.core.pagination.page import Page
from app.features.events.dto.event_search_request import EventSearchRequest
from app.features.events.enums.event_sort import EventSort
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.enums.event_audience import EventAudience
from app.features.events.exceptions.event_exceptions import EventNotFoundError
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event
from app.features.events.models.event_status import EventStatus
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

    async def search(self, request: EventSearchRequest, statuses: set[EventStatusCode] | None, audience: set[EventAudience] | None) -> Page[Event]:
        stmt = select(Event)

        if request.search:
            stmt = stmt.where(
                or_(
                    Event.title.ilike(f"%{request.search}%"),
                    Event.description.ilike(f"%{request.search}%")
                )
            )

        if request.activity_type_id:
            stmt = stmt.where(Event.activity_type_id == request.activity_type_id)

        allowed_statuses = statuses

        if request.statuses is not None:
            if allowed_statuses is None:
                allowed_statuses = request.statuses

            else:
                allowed_statuses = allowed_statuses.intersection(request.statuses)

        if allowed_statuses is not None:
            stmt = (stmt.join(Event.status).where(EventStatus.code.in_(allowed_statuses)))

        if request.starts_after:
            stmt = stmt.where(Event.start_at >= request.starts_after)

        if request.ends_before:
            stmt = stmt.where(Event.end_at <= request.ends_before)

        if audience is not None:
            stmt = stmt.where(Event.audience.in_(audience))

        match request.sort:
            case EventSort.START_DATE_ASC:
                stmt = stmt.order_by(Event.start_at.asc())
            case EventSort.START_DATE_DESC:
                stmt = stmt.order_by(Event.start_at.desc())
            case EventSort.END_DATE_ASC:
                stmt = stmt.order_by(Event.end_at.asc())
            case EventSort.END_DATE_DESC:
                stmt = stmt.order_by(Event.end_at.desc())
            case EventSort.TITLE_ASC:
                stmt = stmt.order_by(Event.title.asc())
            case EventSort.TITLE_DESC:
                stmt = stmt.order_by(Event.title.desc())
            case EventSort.CREATE_DATE_ASC:
                stmt = stmt.order_by(Event.created_at.asc())
            case EventSort.CREATE_DATE_DESC:
                stmt = stmt.order_by(Event.created_at.desc())
            case _:
                stmt = stmt.order_by(Event.start_at.desc())

        return await self.paginate(stmt, request.pagination)

    async def get_audience_required(self, event_id: UUID, audience: EventAudience) -> Event | None:
        stmt = (
            select(Event)
            .where(Event.id == event_id)
            .where(Event.audience == audience)
        )

        return await self._session.scalar(stmt)