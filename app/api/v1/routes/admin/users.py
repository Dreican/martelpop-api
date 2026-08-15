from uuid import UUID

from fastapi import APIRouter, status

from app.core.pagination.page import Page
from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.users.dependencies.routes import UserSearchRequestDep
from app.features.users.dependencies.services import UserServiceDep
from app.features.users.dto.user_admin_response import UserAdminResponse
from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_update_request import UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Admin Users"])


@router.get("/search", response_model=Page[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
        request: UserSearchRequestDep,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_READ)
):
    return await user_service.search(request)


@router.get("/{user_id}", response_model=UserAdminResponse, status_code=status.HTTP_200_OK)
async def get_user(
        user_id: UUID,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_READ)
) -> UserAdminResponse:
    return await user_service.get_user(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserAdminResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
        user_id: UUID,
        request: UserUpdateRequest,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_UPDATE)
) -> UserAdminResponse:
    return await user_service.update(user_id, request, principal)


@router.delete(
    "/{user_id}",
    response_model=UserAdminResponse,
    status_code=status.HTTP_200_OK
)
async def delete_user(
        user_id: UUID,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_DELETE)
) -> UserAdminResponse:
    return await user_service.delete(user_id, principal)
