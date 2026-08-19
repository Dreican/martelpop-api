import logging
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination.page import Page
from app.core.services.base_service import BaseService
from app.core.services.slug_service import SlugService
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.security.principal import AuthenticatedPrincipal, Principal
from app.features.events.dto.requests.event_create_request import EventCreateRequest
from app.features.events.dto.requests.event_participant_request import EventParticipantRequest
from app.features.events.dto.requests.event_search_request import EventSearchRequest
from app.features.events.dto.requests.event_update_request import EventUpdateRequest
from app.features.events.dto.responses.event_response import EventResponse
from app.features.events.dto.responses.participant_response import ParticipantResponse
from app.features.events.exceptions.event_exceptions import EventNotFoundError
from app.features.events.factories.event_response_factory import EventResponseFactory
from app.features.events.factories.participant_response_factory import ParticipantResponseFactory
from app.features.events.filters.event_access_filter import EventAccessFilter
from app.features.events.models.event import Event
from app.features.events.policies.event_policy import EventPolicy
from app.features.events.repositories.activity_type_repository import ActivityTypeRepository
from app.features.events.repositories.event_repository import EventRepository
from app.features.events.repositories.event_status_repository import EventStatusRepository
from app.features.registrations.repositories.registration_repository import RegistrationRepository
from app.features.settings.services.application_settings import ApplicationSettings
from app.features.storage.dto.file_download import FileDownload
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.features.storage.enums.storage_categories import StorageCategory
from app.features.storage.exceptions.storage_exceptions import StorageFileNotFoundError
from app.features.storage.factories.stored_file_response_factory import StoredFileResponseFactory
from app.features.storage.services.file_service import FileService

logger = logging.getLogger(__name__)


class EventService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            event_repository: EventRepository,
            event_status_repository: EventStatusRepository,
            activity_type_repository: ActivityTypeRepository,
            registrations_repository: RegistrationRepository,
            slug_service: SlugService,
            file_service: FileService,
            event_policy: EventPolicy,
            event_access: EventAccessFilter,
            application_settings: ApplicationSettings,
            event_response: EventResponseFactory,
            participant_response: ParticipantResponseFactory,
            stored_file_response: StoredFileResponseFactory,
    ):
        super().__init__(session)
        self._event_repo = event_repository
        self._event_status_repo = event_status_repository
        self._activity_type_repo = activity_type_repository
        self._registrations = registrations_repository
        self._slug = slug_service
        self._file = file_service
        self._policy = event_policy
        self._access = event_access
        self._settings = application_settings
        self._response = event_response
        self._participant_response = participant_response
        self._stored_file_response = stored_file_response

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
        await self._save(event)
        return self._response.create(event)

    async def get_event(self, event_id: UUID, principal: Principal) -> EventResponse:
        event = await self._event_repo.get_required(event_id)
        if not self._policy.can_view(event, principal):
            raise EventNotFoundError(event_id=event_id)

        return self._response.create(event)

    async def get_event_by_slug(self, event_slug: str, principal: Principal) -> EventResponse:
        event = await self._event_repo.required_by_slug(event_slug)
        if not self._policy.can_view(event, principal):
            raise EventNotFoundError(event_slug=event_slug)

        return self._response.create(event)

    async def list_events(self, request: EventSearchRequest, principal: Principal) -> Page[EventResponse]:
        access = self._access.build(principal)
        # access = replace(access, include_deleted=True)
        page = await self._event_repo.search(request, access)

        return page.map(self._response.create)

    async def update_event(self, event_id: UUID, request: EventUpdateRequest,
                           principal: AuthenticatedPrincipal) -> EventResponse:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_edit(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_UPDATE}, user=principal.display_name)

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

    async def delete_event(self, event_id: UUID, principal: AuthenticatedPrincipal) -> EventResponse:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_delete(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_DELETE}, user=principal.user.display_name)

        status = await self._event_status_repo.get_cancelled()
        event.delete(status)

        return await self._persist(event)

    async def publish_event(self, event_id: UUID, principal: AuthenticatedPrincipal) -> EventResponse:
        event = await self._get_publishable_event(event_id, principal)

        status = await self._event_status_repo.get_published()
        event.publish(status)

        return await self._persist(event)

    async def unpublish_event(self, event_id: UUID, principal: AuthenticatedPrincipal) -> EventResponse:
        event = await self._get_publishable_event(event_id, principal)

        status = await self._event_status_repo.get_default()
        event.unpublish(status)

        return await self._persist(event)

    async def cancel_event(self, event_id: UUID, principal: AuthenticatedPrincipal) -> EventResponse:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_cancel(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_CANCEL}, user=principal.display_name)

        status = await self._event_status_repo.get_cancelled()
        event.cancel(status)

        return await self._persist(event)

    async def complete_event(self, event_id: UUID, principal: AuthenticatedPrincipal) -> EventResponse:
        event = await self._event_repo.get_required(event_id)
        if not self._policy.can_complete(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_PUBLISH}, user=principal.display_name)

        status = await self._event_status_repo.get_complete()
        event.complete(status)

        return await self._persist(event)

    async def get_participants(
            self,
            request: EventParticipantRequest,
            principal: AuthenticatedPrincipal
    ) -> Page[ParticipantResponse]:
        event = await self._event_repo.get_required(request.event_id)

        if not self._policy.can_view_participant(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_READ}, user=principal.display_name)

        page = await self._registrations.search_participants(request)

        return self._participant_response.create_page(page)

    async def upload_banner(self, event_id: UUID, principal: AuthenticatedPrincipal,
                            file: UploadFile) -> StoredFileResponse:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_edit(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_UPDATE}, user=principal.display_name)

        old_banner_file_id = event.banner_file_id

        stored_file = await self._file.upload(file, uploaded_by_id=principal.user.id,
                                              category=StorageCategory.EVENTS_BANNER)

        try:
            event.banner_file_id = stored_file.id
            await self._flush()
            await self._refresh(event)
        except Exception:
            await self._file.delete(stored_file.id)
            raise

        if old_banner_file_id is not None:
            await self._file.delete(old_banner_file_id)
            await self._flush()

        return self._stored_file_response.create(stored_file)

    async def delete_banner(self, event_id: UUID, principal: AuthenticatedPrincipal) -> None:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_edit(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_UPDATE}, user=principal.display_name)

        old_file_id = event.banner_file_id

        if old_file_id is None:
            return

        event.banner_file_id = None
        await self._session.flush()
        await self._file.delete(old_file_id)

    async def get_banner(self, event_slug: str, principal: Principal) -> FileDownload:
        event = await self._event_repo.required_by_slug(event_slug)

        if not self._policy.can_view(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_READ}, user=principal.display_name)

        if event.banner_file_id is None:
            raise StorageFileNotFoundError(f"Event {event_slug} does not have a banner.")

        file, content = await self._file.download(event.banner_file_id)

        return FileDownload(file=file, content=content, is_public=event.is_public)

    async def _persist(self, event: Event) -> EventResponse:
        await self._commit()
        await self._refresh(event)

        return self._response.create(event)

    async def _get_publishable_event(self, event_id: UUID, principal: AuthenticatedPrincipal) -> Event:
        event = await self._event_repo.get_required(event_id)

        if not self._policy.can_edit(event, principal):
            raise PermissionDeniedError(permissions={PermissionCode.EVENT_PUBLISH}, user=principal.display_name)

        return event
