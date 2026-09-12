import logging
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.base_service import BaseService
from app.core.services.slug_service import SlugService
from app.features.auth.security.principal import AuthenticatedPrincipal, Principal
from app.features.events.dto.requests.activity_type_create_request import ActivityTypeCreateRequest
from app.features.events.dto.requests.activity_type_update_request import ActivityTypeUpdateRequest
from app.features.events.dto.responses.activity_type_admin_response import ActivityTypeAdminResponse
from app.features.events.dto.responses.activity_type_response import ActivityTypeResponse
from app.features.events.factories.activity_type_admin_response_factory import ActivityTypeAdminResponseFactory
from app.features.events.factories.activity_type_response_factory import ActivityTypeResponseFactory
from app.features.events.factories.activity_type_summary_response_factory import ActivityTypeSummaryResponseFactory
from app.features.events.models.activity_type import ActivityType
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
            response_summary_factory: ActivityTypeSummaryResponseFactory,
            response_factory: ActivityTypeResponseFactory,
            response_admin_factory: ActivityTypeAdminResponseFactory,
    ):
        super().__init__(session)
        self._activity_type_repo = activity_type_repository
        self._slug = slug_service
        self._file = file_service
        self._settings = application_settings
        self._stored_file_response = stored_file_response
        self._response_summary = response_summary_factory
        self._response = response_factory
        self._response_admin = response_admin_factory

    async def create_activity_type(
            self, request: ActivityTypeCreateRequest, principal: AuthenticatedPrincipal
            ) -> ActivityTypeAdminResponse:

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

    async def get_activity_type_by_slug(self, activity_type_slug: str) -> ActivityTypeResponse:
        activity_type = await self._activity_type_repo.required_by_slug(activity_type_slug)

        return self._response.create(activity_type)

    async def list_activity_type(self) -> list[ActivityTypeAdminResponse]:
        activity_types = await self._activity_type_repo.get_all()

        return self._response_admin.create_many(activity_types)

    async def update_activity_type(
            self, activity_type_id: UUID, request: ActivityTypeUpdateRequest
            ) -> ActivityTypeAdminResponse:
        activity_type = await self._activity_type_repo.get_required(activity_type_id)

        if activity_type.name != request.name:
            activity_type.slug = await self._slug.create_unique(
                request.name, slug_exists=self._activity_type_repo.exists_by_slug
                )

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

    async def upload_icon(
            self,
            activity_type_id: UUID,
            principal: AuthenticatedPrincipal,
            file: UploadFile
    ) -> StoredFileResponse:
        activity_type = await self._activity_type_repo.get_required(activity_type_id)

        old_icon_file_id = activity_type.icon_file_id

        stored_file = await self._file.upload(
            file,
            uploaded_by_id=principal.user.id,
            category=StorageCategory.ACTIVITY_TYPE_ICON
        )

        try:
            activity_type.icon_file_id = stored_file.id
            await self._commit()
        except Exception:
            await self._file.delete(stored_file.id)
            raise

        if old_icon_file_id is not None:
            await self._file.delete(old_icon_file_id)
            await self._commit()

        return self._stored_file_response.create(stored_file)

    async def delete_icon(self, activity_type_id: UUID) -> None:
        activity_type = await self._activity_type_repo.get_required(activity_type_id)

        old_icon_file_id = activity_type.icon_file_id

        if old_icon_file_id is None:
            return

        activity_type.icon_file_id = None
        await self._commit()
        await self._file.delete(old_icon_file_id)
        await self._commit()

    async def get_icon(self, activity_type_slug: str) -> FileDownload:
        activity_type = await self._activity_type_repo.required_by_slug(activity_type_slug)

        if activity_type.icon_file_id is None:
            raise StorageFileNotFoundError(f"Activity type {activity_type_slug} does not have an icon.")

        file, content = await self._file.download(activity_type.icon_file_id)

        return FileDownload(file=file, content=content, is_public=True)

    async def _persist(self, activity_type: ActivityType) -> ActivityTypeAdminResponse:
        await self._commit()
        await self._refresh(activity_type)

        return self._response_admin.create(activity_type)
