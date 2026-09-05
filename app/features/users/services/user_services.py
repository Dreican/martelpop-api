from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination.page import Page
from app.core.services.base_service import BaseService
from app.core.services.slug_service import SlugService
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.auth.security.principal import AuthenticatedPrincipal, Principal
from app.features.storage.dto.file_download import FileDownload
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.features.storage.enums.storage_categories import StorageCategory
from app.features.storage.exceptions.storage_exceptions import StorageFileNotFoundError
from app.features.storage.factories.stored_file_response_factory import StoredFileResponseFactory
from app.features.storage.services.file_service import FileService
from app.features.users.dto.user_admin_response import UserAdminResponse
from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_search_request import UserSearchRequest
from app.features.users.dto.user_summary_response import UserSummaryResponse
from app.features.users.dto.user_update_request import UserUpdateRequest
from app.features.users.factories.user_admin_response_factory import UserAdminResponseFactory
from app.features.users.factories.user_response_factory import UserResponseFactory
from app.features.users.factories.user_summary_response_factory import UserSummaryResponseFactory
from app.features.users.models.user import User
from app.features.users.repositories.user_repository import UserRepository


class UserService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            slug_service: SlugService,
            file_service: FileService,
            user_response: UserResponseFactory,
            user_admin_response: UserAdminResponseFactory,
            user_summary_response: UserSummaryResponseFactory,
            store_file_response: StoredFileResponseFactory
    ):
        super().__init__(session)
        self._users = user_repository
        self._roles = role_repository
        self._slug = slug_service
        self._file = file_service
        self._user_summary_response = user_summary_response
        self._user_response = user_response
        self._user_admin_response = user_admin_response
        self._store_file_response = store_file_response

    async def me(self, principal: AuthenticatedPrincipal) -> UserResponse:
        return self._user_response.create(principal.user)

    async def search(self, request: UserSearchRequest) -> Page[UserResponse]:
        return self._user_response.create_page(await self._users.search(request))

    async def get_user(self, user_id: UUID) -> UserAdminResponse:
        return self._user_admin_response.create(await self._users.get_required(user_id))

    async def get_user_slug(self, user_slug: str) -> UserSummaryResponse:
        return self._user_summary_response.create(await self._users.required_by_slug(user_slug))

    async def update(
            self,
            user_id: UUID,
            request: UserUpdateRequest
    ) -> UserAdminResponse:
        user = await self._users.get_required(user_id)
        old_display_name = user.display_name
        user.update(request)

        await self._update_slug_if_needed(user, old_display_name)

        return await self._persist(user)

    async def update_me(self, request: UserUpdateRequest, principal: AuthenticatedPrincipal) -> UserResponse:
        user = principal.user
        old_display_name = user.display_name
        user.update(request)

        await self._update_slug_if_needed(user, old_display_name)

        await self._commit()
        await self._refresh(user)

        return self._user_response.create(user)

    async def _update_slug_if_needed(self, user: User, old_display_name: str) -> None:
        if user.display_name != old_display_name:
            user.slug = await self._slug.create_unique(
                user.display_name,
                slug_exists=self._users.exists_by_slug,
            )

    async def delete(self, user_id: UUID) -> UserAdminResponse:
        user = await self._users.get_required(user_id)

        user.delete()

        return await self._persist(user)

    async def delete_me(self, principal: AuthenticatedPrincipal) -> UserAdminResponse:
        user = await self._users.get_required(principal.user.id)

        user.delete()

        return await self._persist(user)

    async def upload_avatar(self, user_id: UUID, principal: AuthenticatedPrincipal, file: UploadFile) -> StoredFileResponse:
        user = await self._users.get_required(user_id)
        return await self._upload_user_avatar(user, principal, file)

    async def upload_avatar_me(self, principal: AuthenticatedPrincipal, file: UploadFile) -> StoredFileResponse:
        user = await self._users.get_required(principal.user.id)
        return await self._upload_user_avatar(user, principal, file)

    async def delete_avatar(self, user_id: UUID) -> None:
        user = await self._users.get_required(user_id)
        await self._delete_user_avatar(user)

    async def delete_avatar_me(self, principal: AuthenticatedPrincipal) -> None:
        user = await self._users.get_required(principal.user.id)
        await self._delete_user_avatar(user)

    async def get_avatar(self, user_slug: str) -> FileDownload:
        user = await self._users.required_by_slug(user_slug)

        if user.avatar_file_id is None:
            raise StorageFileNotFoundError(f"User {user_slug} does not have an avatar.")

        file, content = await self._file.download(user.avatar_file_id)

        return FileDownload(file=file, content=content, is_public=True)

    async def _persist(self, user: User) -> UserAdminResponse:
        await self._commit()
        await self._refresh(user)

        return self._user_admin_response.create(user)

    async def _upload_user_avatar(self, user: User, principal: AuthenticatedPrincipal, file: UploadFile) -> StoredFileResponse:
        old_file_id = user.avatar_file_id

        avatar = await self._file.upload(file, uploaded_by_id=principal.user.id, category=StorageCategory.USER_AVATARS)

        try:
            user.avatar_file_id = avatar.id
            await self._commit()
        except Exception:
            await self._file.delete(avatar.id)
            raise

        if old_file_id is not None:
            await self._file.delete(old_file_id)
            await self._commit()

        return self._store_file_response.create(avatar)

    async def _delete_user_avatar(self, user: User) -> None:
        avatar_id = user.avatar_file_id

        if avatar_id is None:
            return

        user.avatar_file_id = None
        await self._commit()
        await self._file.delete(avatar_id)
        await self._commit()