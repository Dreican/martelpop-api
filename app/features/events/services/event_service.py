import logging
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination.page import Page
from app.core.services.base_service import BaseService
from app.core.services.slug_service import SlugService
from app.features.auth.dependencies.current_principal import CurrentPrincipal, AuthenticatedPrincipal
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.events.dto.event_create_request import EventCreateRequest
from app.features.events.dto.event_response import EventResponse
from app.features.events.dto.event_search_request import EventSearchRequest
from app.features.events.dto.event_update_request import EventUpdateRequest
from app.features.events.exceptions.event_exceptions import EventNotFoundError
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event
from app.features.events.policies.event_policy import EventPolicy
from app.features.events.repositories.activity_type_repository import ActivityTypeRepository
from app.features.events.repositories.event_repository import EventRepository
from app.features.events.repositories.event_status_repository import EventStatusRepository
from app.features.users.models.user import User

logger = logging.getLogger(__name__)


class EventService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            event_repository: EventRepository,
            event_status_repository: EventStatusRepository,
            activity_type_repository: ActivityTypeRepository,
            slug_service: SlugService,
            event_policy: EventPolicy
    ):
        super().__init__(session)
        self._event_repo = event_repository
        self._event_status_repo = event_status_repository
        self._activity_type_repo = activity_type_repository
        self._slug = slug_service
        self._policy = event_policy

    async def create_event(self, request: EventCreateRequest, principal: AuthenticatedPrincipal) -> EventResponse:
        default_status = await self._event_status_repo.get_default()
        activity_type = await self._activity_type_repo.get_required(request.activity_type_id)
        slug = await self._slug.create_unique(request.title, slug_exists=self._event_repo.exists_by_slug)

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
            creator=principal.user,
        )

        await self._event_repo.add(event)
        await self._flush()
        await self._refresh(event)
        return EventResponse.model_validate(event)


    async def get_event(self, event_id: UUID, principal: CurrentPrincipal) -> EventResponse:
        event = await self._event_repo.get_required(event_id)
        if not self._policy.can_view(event, principal.user):
            raise EventNotFoundError(event_id=event_id)

        return EventResponse.model_validate(event)

    async def get_event_by_slug(self, event_slug: str, principal: CurrentPrincipal) -> EventResponse:
        event = await self._event_repo.required_by_slug(event_slug)
        if not self._policy.can_view(event, principal.user):
            raise EventNotFoundError(event_slug=event_slug)

        return EventResponse.model_validate(event)


    async def list_events(self, request: EventSearchRequest, principal: CurrentPrincipal) -> Page[EventResponse]:
        statuses = self._policy.visible_statuses(principal.user)
        audience = self._policy.visible_audiences(principal.user)
        page = await self._event_repo.search(request, statuses, audience)

        return page.map(EventResponse.model_validate)

    async def update_event(self, event_id: UUID, request: EventUpdateRequest, principal: AuthenticatedPrincipal) -> EventResponse:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_edit(event, principal.user):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_UPDATE}, user=principal.user.display_name)

        if event.title != request.title:
            event.slug = await self._slug.create_unique(request.title, slug_exists=self._event_repo.exists_by_slug)

        event.update(
            title=request.title,
            description=request.description,
            location=request.location,
            start_at=request.start_at,
            end_at=request.end_at,
            capacity=request.capacity
        )

        return await self._persist(event)

    async def delete_event(self, event_id: UUID, user: User) -> EventResponse:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_delete(event, user):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_DELETE}, user=user.email)

        event.delete()

        return await self._persist(event)

    async def publish_event(self, event_id: UUID, user: User) -> EventResponse:
        event = await self._get_publishable_event(event_id, user)

        status = await self._event_status_repo.get_published()
        event.publish(status)

        return await self._persist(event)

    async def unpublish_event(self, event_id: UUID, user: User) -> EventResponse:
        event = await self._get_publishable_event(event_id, user)

        status = await self._event_status_repo.get_default()
        event.unpublish(status)

        return await self._persist(event)

    async def cancel_event(self, event_id: UUID, user: User) -> EventResponse:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_cancel(event, user):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_UPDATE}, user=user.email)

        status = await self._event_status_repo.get_cancelled()
        event.cancel(status)

        return await self._persist(event)

    async def complete_event(self, event_id: UUID, user: User) -> EventResponse:
        event = await self._event_repo.get_required(event_id)
        if not self._policy.can_complete(event, user):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_PUBLISH}, user=user.email)

        status = await self._event_status_repo.get_complete()
        event.complete(status)

        return await self._persist(event)

    async def _persist(self, event: Event) -> EventResponse:
        await self._commit()
        await self._refresh(event)

        return EventResponse.model_validate(event)

    async def _get_publishable_event(self, event_id: UUID, user: User) -> Event:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_edit(event, user):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_PUBLISH}, user=user.email)

        return event