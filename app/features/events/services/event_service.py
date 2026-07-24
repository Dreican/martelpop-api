import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.slug_service import SlugService

from app.features.events.dto.create_event_request import CreateEventRequest
from app.features.events.dto.event_response import EventResponse
from app.features.events.exceptions.activity_type_exceptions import ActivityTypeNotFoundError
from app.features.events.exceptions.event_status_exceptions import DefaultEventStatusNotFoundError
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event
from app.features.events.repositories.activity_type_repository import ActivityTypeRepository
from app.features.events.repositories.event_repository import EventRepository
from app.features.events.repositories.event_status_repository import EventStatusRepository
from app.features.users.models.user import User

logger = logging.getLogger(__name__)


class EventService:
    def __init__(
            self,
            session: AsyncSession,
            event_repository: EventRepository,
            event_status_repository: EventStatusRepository,
            activity_type_repository: ActivityTypeRepository,
            slug_service: SlugService,
    ):
        self._session = session
        self._event_repo = event_repository
        self._event_status_repo = event_status_repository
        self._activity_type_repo = activity_type_repository
        self._slug = slug_service

    async def create_event(self, request: CreateEventRequest, creator: User) -> Event:
        try:
            default_status = await self._event_status_repo.get_default()
            activity_type = await self._activity_type_repo.get_required(request.activity_type_id)
            slug = await self._slug.create_unique(request.title, slug_exists=self._activity_type_repo.exists_by_slug)

            event = Event(
                title=request.title,
                slug=slug,
                description=request.description,
                location=request.location,
                start_at=request.starts_at,
                end_at=request.ends_at,
                capacity=request.capacity,
                activity_type=activity_type,
                status=default_status,
                creator=creator,
            )

            await self._event_repo.add(event)
            await self._session.commit()
            await self._session.refresh(event)
            return event

        except Exception:
            await self._session.rollback()
            raise

    async def get_event(self, event_id: UUID) -> EventResponse:
        return await self._event_repo.get_by_id(event_id)

    async def get_event_by_activity_type(self, activity_type: ActivityType):
        return await self._event_repo.get_by_activity_type(activity_type)