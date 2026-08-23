from typing import Any
from uuid import UUID

from sqlalchemy import select, Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database.repositories.base_repository import BaseRepository
from app.core.pagination.page import Page
from app.features.events.dto.requests.event_participant_request import EventParticipantRequest
from app.features.events.models.event import Event
from app.features.registrations.dto.requests.registration_search_request import RegistrationSearchRequest
from app.features.registrations.enums.registration_sort import RegistrationSort
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.registrations.exceptions.registrations_exceptions import RegistrationNotFoundError
from app.features.registrations.models.registration import Registration


class RegistrationRepository(BaseRepository[Registration]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=Registration, not_found_exception=RegistrationNotFoundError)

    async def get_required(self, entity_id: UUID) -> Registration:
        stmt = (
            select(Registration)
            .where(Registration.id == entity_id)
        )
        stmt = self._with_summary_graph(stmt)
        registration = await self._session.scalar(stmt)

        if not registration:
            raise RegistrationNotFoundError(entity_id=entity_id)

        return registration

    async def get_by_status(self, registration_status: RegistrationStatus) -> list[Registration]:
        stmt = (
            select(Registration).where(Registration.status == registration_status)
        )

        return list(await self._session.scalars(stmt))

    async def exists(self, event_id: UUID, user_id: UUID) -> bool:
        stmt = (
            select(1)
            .where(Registration.event_id == event_id)
            .where(Registration.user_id == user_id)
            .exists()
        )

        already_registered = await self._session.scalar(select(stmt))

        return bool(already_registered)

    @staticmethod
    async def cancel(registration: Registration) -> None:
        registration.status = RegistrationStatus.CANCELLED

    async def search_by_user(self, request: RegistrationSearchRequest, user_id: UUID) -> Page[Registration]:
        stmt = (
            select(Registration)
            .where(Registration.user_id == user_id)
        )

        stmt = self._with_detail_graph(stmt)
        stmt = self._apply_filter(stmt, request)
        stmt = self._apply_sort(stmt, request.sort)

        return await self.paginate(stmt, request.pagination)

    async def search_participants(self, request: EventParticipantRequest) -> Page[Registration]:
        stmt = (
            select(Registration)
            .options(selectinload(Registration.user))
            .where(Registration.event_id == request.event_id)
        )

        if not request.include_cancelled:
            stmt = stmt.where(
                Registration.status != RegistrationStatus.CANCELLED
            )

        stmt = self._apply_sort(stmt, request.sort)

        return await self.paginate(stmt, request.pagination)

    @staticmethod
    def _with_summary_graph(stmt: Select[tuple[Any]]) -> Select[tuple[Registration]]:
        return stmt.options(
            selectinload(Registration.event).selectinload(Event.activity_type),
            selectinload(Registration.event).selectinload(Event.status),
            selectinload(Registration.user),
        )

    @staticmethod
    def _with_detail_graph(stmt: Select[tuple[Any]]) -> Select[tuple[Registration]]:
        return stmt.options(
            selectinload(Registration.event).selectinload(Event.activity_type),
            selectinload(Registration.event).selectinload(Event.status),
            selectinload(Registration.user),
        )

    @staticmethod
    def _apply_filter(
            stmt: Select[tuple[Any]],
            request: RegistrationSearchRequest
    ) -> Select[tuple[Any]]:

        if request.statuses is not None:
            stmt = stmt.where(Registration.status.in_(request.statuses))

        return stmt

    @staticmethod
    def _apply_sort(stmt: Select[tuple[Any]], sort: RegistrationSort) -> Select[tuple[Any]]:
        sorts = {
            RegistrationSort.REGISTRATION_DATE_ASC: Registration.created_at.asc(),
            RegistrationSort.REGISTRATION_DATE_DESC: Registration.created_at.desc(),
            RegistrationSort.CANCELLED_REGISTRATION_DATE_ASC: Registration.cancelled_at.asc(),
            RegistrationSort.CANCELLED_REGISTRATION_DATE_DESC: Registration.cancelled_at.desc(),
            RegistrationSort.REGISTRATION_STATUS_ASC: Registration.status.asc(),
            RegistrationSort.REGISTRATION_STATUS_DESC: Registration.status.desc(),

        }

        stmt = stmt.order_by(
            sorts.get(
                sort,
                Registration.created_at.desc(),
            )
        )

        return stmt
