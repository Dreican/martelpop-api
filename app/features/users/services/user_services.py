from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination.page import Page
from app.core.services.base_service import BaseService
from app.core.services.slug_service import SlugService
from app.core.storage.file_categories import FileCategory
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.features.storage.models.stored_file import StoredFile
from app.features.storage.services.file_service import FileService
from app.features.users.dto.user_admin_response import UserAdminResponse
from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_search_request import UserSearchRequest
from app.features.users.dto.user_update_request import UserUpdateRequest
from app.features.users.factories.user_admin_response_factory import UserAdminResponseFactory
from app.features.users.factories.user_response_factory import UserResponseFactory
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
            user_admin_response: UserAdminResponseFactory
    ):
        super().__init__(session)
        self._users = user_repository
        self._roles = role_repository
        self._slug = slug_service
        self._file = file_service
        self._user_response = user_response
        self._user_admin_response = user_admin_response

    async def me(self, principal: AuthenticatedPrincipal) -> UserAdminResponse:
        return self._user_admin_response.create(principal.user)

    async def search(self, request: UserSearchRequest) -> Page[UserResponse]:
        return self._user_response.create_page(await self._users.search(request))

    async def get_user(self, user_id: UUID) -> UserAdminResponse:
        return self._user_admin_response.create(await self._users.get_required(user_id))

    async def get_user_slug(self, user_slug: str) -> UserResponse:
        return self._user_response.create(await self._users.required_by_slug(user_slug))

    async def update(
            self,
            user_id: UUID,
            request: UserUpdateRequest,
            principal: AuthenticatedPrincipal
    ) -> UserAdminResponse:
        if not self._can_manage_user(principal, user_id):
            raise PermissionDeniedError(permissions={PermissionCode.USER_UPDATE}, user=principal.user.display_name)

        user = await self._users.get_required(user_id)
        old_display_name = user.display_name
        user.update(request)

        await self._update_slug_if_needed(user, old_display_name)

        return await self._persist(user)

    async def update_me(self, request: UserUpdateRequest, principal: AuthenticatedPrincipal) -> UserAdminResponse:
        if not self._can_manage_user(principal, principal.user.id):
            raise PermissionDeniedError(permissions={PermissionCode.USER_UPDATE}, user=principal.user.display_name)

        user = principal.user
        old_display_name = user.display_name
        user.update(request)

        await self._update_slug_if_needed(user, old_display_name)

        return await self._persist(user)

    async def _update_slug_if_needed(self, user: User, old_display_name: str) -> None:
        if user.display_name != old_display_name:
            user.slug = await self._slug.create_unique(
                user.display_name,
                slug_exists=self._users.exists_by_slug,
            )

    async def delete(self, user_id: UUID, principal: AuthenticatedPrincipal) -> UserAdminResponse:
        if not self._can_manage_user(principal, user_id):
            raise PermissionDeniedError(permissions={PermissionCode.USER_DELETE}, user=principal.user.display_name)

        user = await self._users.get_required(user_id)

        user.delete()

        return await self._persist(user)

    async def delete_me(self, principal: AuthenticatedPrincipal) -> UserAdminResponse:
        if not self._can_manage_user(principal, principal.user.id):
            raise PermissionDeniedError(permissions={PermissionCode.USER_DELETE}, user=principal.user.display_name)

        user = await self._users.get_required(principal.user.id)

        user.delete()

        return await self._persist(user)

    async def upload_avatar(self, principal: AuthenticatedPrincipal, file: UploadFile) -> StoredFileResponse:
        if not self._can_manage_user(principal, principal.user.id):
            raise PermissionDeniedError(permissions={PermissionCode.USER_UPDATE}, user=principal.user.display_name)

        user = await self._users.get_required(principal.user.id)
        old_file_id = user.avatar_file_id

        avatar = await self._file.upload(file, uploaded_by_id=principal.user.id, category=FileCategory.USER_AVATAR)

        try:
            user.avatar_file_id = avatar.id
            await self._flush()
            await self._refresh(user)
        except Exception:
            await self._file.delete(avatar.id)
            raise

        if old_file_id is not None:
            await self._file.delete(old_file_id)
            await self._flush()

        return StoredFileResponse.model_validate(avatar)

    async def delete_avatar(self, principal: AuthenticatedPrincipal) -> None:
        user = await self._users.get_required(principal.user.id)

        avatar_id = user.avatar_file_id

        if avatar_id is None:
            return

        user.avatar_file_id = None
        await self._flush()
        await self._file.delete(avatar_id)

    @staticmethod
    def _can_manage_user(principal: AuthenticatedPrincipal, user_id: UUID) -> bool:
        return principal.is_admin or principal.user.id == user_id

    async def _persist(self, user: User) -> UserAdminResponse:
        await self._commit()
        await self._refresh(user)

        return self._user_admin_response.create(user)