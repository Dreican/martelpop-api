from fastapi import APIRouter, status

from app.features.auth.dependencies.current_principal import AuthenticatedPrincipalDep
from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.users.dependencies.services import UserServiceDep
from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_update_request import UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def me(principal: AuthenticatedPrincipalDep, user_service: UserServiceDep, ) -> UserResponse:
    return await user_service.me(principal)


@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
        request: UserUpdateRequest,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_UPDATE)
) -> UserResponse:
    return await user_service.update_me(request, principal)


@router.delete("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def delete_user(
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_DELETE)
) -> UserResponse:
    return await user_service.delete_me(principal)
