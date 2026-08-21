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
from app.features.events.dto.requests.activity_type_create_request import ActivityTypeCreateRequest
from app.features.events.dto.requests.activity_type_update_request import ActivityTypeUpdateRequest
from app.features.events.dto.requests.event_participant_request import EventParticipantRequest
from app.features.events.dto.requests.event_update_request import EventUpdateRequest
from app.features.events.dto.responses.activity_type_admin_response import ActivityTypeAdminResponse
from app.features.events.dto.responses.activity_type_response import ActivityTypeResponse
from app.features.events.dto.responses.event_response import EventResponse
from app.features.events.dto.responses.participant_response import ParticipantResponse
from app.features.events.factories.activity_type_admin_response_factory import ActivityTypeAdminResponseFactory
from app.features.events.models.activity_type import ActivityType
from app.features.events.models.event import Event
from app.features.events.repositories.activity_type_repository import ActivityTypeRepository
from app.features.settings.services.application_settings import ApplicationSettings
from app.features.storage.dto.file_download import FileDownload
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.features.storage.enums.storage_categories import StorageCategory
from app.features.storage.exceptions.storage_exceptions import StorageFileNotFoundError
from app.features.storage.factories.stored_file_response_factory import StoredFileResponseFactory
from app.features.storage.services.file_service import FileService

logger = logging.getLogger(__name__)


class ActivityTypeService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            activity_type_repository: ActivityTypeRepository,
            slug_service: SlugService,
            file_service: FileService,
            application_settings: ApplicationSettings,
            stored_file_response: StoredFileResponseFactory,
            response_admin_factory: ActivityTypeAdminResponseFactory,
    ):
        super().__init__(session)
        self._activity_type_repo = activity_type_repository
        self._slug = slug_service
        self._file = file_service
        self._settings = application_settings
        self._stored_file_response = stored_file_response
        self._response_admin = response_admin_factory

    async def create_activity_type(self, request: ActivityTypeCreateRequest, principal: AuthenticatedPrincipal) -> ActivityTypeAdminResponse:

        slug = await self._slug.create_unique(request.name, slug_exists=self._activity_type_repo.exists_by_slug)

        activity_type = ActivityType(
            name=request.name,
            slug=slug,
            description=request.description,
            color=request.color,
            default_location=request.default_location,
            default_capacity=request.default_capacity,
            default_duration_minutes=request.default_duration_minutes,
        )

        await self._activity_type_repo.add(activity_type)
        await self._save(activity_type)
        return self._response_admin.create(activity_type)

    async def get_activity_type(self, activity_type_id: UUID) -> ActivityTypeAdminResponse:
        activity_type = await self._activity_type_repo.get_required(activity_type_id)

        return self._response_admin.create(activity_type)

    async def get_activity_type_by_slug(self, event_slug: str, principal: Principal) -> ActivityTypeAdminResponse:
        activity_type = await self._activity_type_repo.required_by_slug(event_slug)

        return self._response_admin.create(activity_type)

    async def list_activity_type(self) -> list[ActivityTypeAdminResponse]:
        activity_types = await self._activity_type_repo.get_all()

        return self._response_admin .create_many(activity_types)

    async def update_activity_type(self, activity_type_id: UUID, request: ActivityTypeUpdateRequest) -> ActivityTypeAdminResponse:
        activity_type = await self._activity_type_repo.get_required(activity_type_id)

        if activity_type.name != request.name:
            activity_type.slug = await self._slug.create_unique(request.name, slug_exists=self._activity_type_repo.exists_by_slug)

        activity_type.update(
            name=request.name,
            description=request.description,
            color=request.color,
            default_location=request.default_location,
            default_capacity=request.default_capacity,
            default_duration_minutes=request.default_duration_minutes
        )

        return await self._persist(activity_type)

    async def delete_activity_type(self, activity_type_id: UUID) -> ActivityTypeResponse:
        activity_type = await self._activity_type_repo.get_required(activity_type_id)
        activity_type.delete()

        return await self._persist(activity_type)

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

        stored_file = await self._file.upload(
            file,
            uploaded_by_id=principal.user.id,
            category=StorageCategory.EVENTS_BANNER
        )

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

    async def _persist(self, activity_type: ActivityType) -> ActivityTypeAdminResponse:
        await self._commit()
        await self._refresh(activity_type)

        return self._response_admin.create(activity_type)
