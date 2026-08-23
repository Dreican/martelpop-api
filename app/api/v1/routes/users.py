from fastapi import APIRouter, status, UploadFile, File
from starlette.responses import StreamingResponse

from app.api.v1.utils.file_response import file_stream_response
from app.features.auth.dependencies.require_permissions import authenticated_permission, permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal, Principal
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.core.http.content_disposition import content_disposition_inline
from app.features.users.dependencies.services import UserServiceDep
from app.features.users.dto.user_admin_response import UserAdminResponse
from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_update_request import UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserAdminResponse
)
async def me(
        user_service: UserServiceDep, principal: AuthenticatedPrincipal = authenticated_permission()
        ) -> UserAdminResponse:
    return await user_service.me(principal)


@router.get(
    "/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def get_user(
        slug: str,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_READ)
) -> UserResponse:
    return await user_service.get_user_slug(slug)


@router.patch(
    "/me",
    response_model=UserAdminResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
        request: UserUpdateRequest,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission()
) -> UserAdminResponse:
    return await user_service.update_me(request, principal)


@router.delete(
    "/me",
    response_model=UserAdminResponse,
    status_code=status.HTTP_200_OK
)
async def delete_user(
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission()
) -> UserAdminResponse:
    return await user_service.delete_me(principal)


@router.post("/me/avatar", response_model=StoredFileResponse, status_code=status.HTTP_201_CREATED)
async def update_avatar(
        user_service: UserServiceDep,
        file: UploadFile = File(...),
        principal: AuthenticatedPrincipal = authenticated_permission()
) -> StoredFileResponse:
    return await user_service.upload_avatar(principal, file)


@router.delete("/me/avatar", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avatar(
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission()
) -> None:
    return await user_service.delete_avatar(principal)


@router.get("/{user_slug}/avatar")
async def get_avatar(
        user_slug: str,
        user_service: UserServiceDep,
        principal: Principal = permission()
) -> StreamingResponse:
    download = await user_service.get_avatar(user_slug, principal)

    return file_stream_response(download)
