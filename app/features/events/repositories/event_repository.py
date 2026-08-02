import logging
from datetime import datetime, UTC
from typing import Any
from uuid import UUID

from sqlalchemy import select, or_, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.repositories.sluggable_repository import SluggableRepository
from app.core.pagination.page import Page
from app.features.events.dto.event_search_request import EventSearchRequest
from app.features.events.enums.event_audience import EventAudience
from app.features.events.enums.event_sort import EventSort
from app.features.events.enums.event_status_code import EventStatusCode
from app.features.events.exceptions.event_exceptions import EventNotFoundError
from app.features.events.filters.event_access import EventAccess
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event
from app.features.events.models.event_status import EventStatus

logger = logging.getLogger(__name__)


class EventRepository(SluggableRepository[Event]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Event, not_found_exception=EventNotFoundError)

    async def required_by_id_with_registration(self, entity_id: UUID) -> Event:
        stmt = (
            select(Event)
            .options(selectinload(Event.registrations))
            .where(Event.id == entity_id)
        )

        event = await self._session.scalar(stmt)

        if event is None:
            raise self._not_found_exception(event_id=entity_id)

        assert event is not None

        return event

    async def get_by_id_with_activity(self, entity_id: UUID) -> Event | None:
        stmt = (
            select(Event)
            .options(selectinload(Event.activity_type))
            .where(ActivityType.id == entity_id)
        )
        return await self._session.scalar(stmt)

    async def get_by_activity_type(self, activity_type_id: UUID) -> list[Event]:
        stmt = (
            select(Event)
            .where(Event.activity_type_id == activity_type_id)
        )

        return list(await self._session.scalars(stmt))

    async def get_upcoming(self) -> list[Event]:
        stmt = (
            select(Event)
            .join(Event.status)
            .where(
                Event.start_at > datetime.now(UTC),
                EventStatus.code == EventStatusCode.PUBLISHED
            )
        )

        return list(await self._session.scalars(stmt))

    async def get_all(self) -> list[Event]:
        stmt = (
            select(Event)
        )
        return list(await self._session.scalars(stmt))

    async def search(self, request: EventSearchRequest, access: EventAccess) -> Page[Event]:
        stmt = select(Event)

        stmt = self._apply_access_filter(stmt, request, access)
        stmt = self._apply_filters(stmt, request)
        stmt = self._apply_sort(stmt, request.sort)

        return await self.paginate(stmt, request.pagination)


    async def get_audience_required(self, event_id: UUID, audience: EventAudience) -> Event | None:
        stmt = (
            select(Event)
            .where(Event.id == event_id)
            .where(Event.audience == audience)
        )

        return await self._session.scalar(stmt)

    @staticmethod
    def _apply_filters(stmt: Select[tuple[Any]], request: EventSearchRequest) -> Select[tuple[Any]]:
        if request.search:
            stmt = stmt.where(
                or_(
                    Event.title.ilike(f"%{request.search}%"),
                    Event.description.ilike(f"%{request.search}%")
                )
            )

        if request.activity_type_id:
            stmt = stmt.where(Event.activity_type_id == request.activity_type_id)

        if request.starts_after:
            stmt = stmt.where(Event.start_at >= request.starts_after)

        if request.ends_before:
            stmt = stmt.where(Event.end_at <= request.ends_before)
        return stmt

    @staticmethod
    def _apply_access_filter(
            stmt: Select[tuple[Any]],
            request: EventSearchRequest,
            access: EventAccess
    ) -> Select[tuple[Any]]:

        if not access.include_deleted:
            stmt = stmt.where(Event.deleted_at.is_(None))

        stmt = (stmt.join(Event.status).where(
            EventStatus.code.in_(access.allowed_statuses(request.statuses))
        ))
        stmt = stmt.where(Event.audience.in_(access.audiences))
        return stmt

    @staticmethod
    def _apply_sort(stmt: Select[tuple[Any]], sort: EventSort) -> Select[tuple[Any]]:
        sorts = {
            EventSort.START_DATE_ASC: Event.start_at.asc(),
            EventSort.START_DATE_DESC: Event.start_at.desc(),
            EventSort.END_DATE_ASC: Event.end_at.asc(),
            EventSort.END_DATE_DESC: Event.end_at.desc(),
            EventSort.TITLE_ASC: Event.title.asc(),
            EventSort.TITLE_DESC: Event.title.desc(),
            EventSort.CREATE_DATE_ASC: Event.created_at.asc(),
            EventSort.CREATE_DATE_DESC: Event.created_at.desc(),
        }

        stmt = stmt.order_by(
            sorts.get(
                sort,
                Event.start_at.desc(),
            )
        )

        return stmt

