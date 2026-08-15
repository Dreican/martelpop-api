from fastapi import APIRouter, status

from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.users.dependencies.services import UserServiceDep
from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_search_request import UserSearchRequest

router = APIRouter(prefix="/users", tags=["Admin Users"])


@router.get("/search", response_model=list(UserResponse), status_code=status.HTTP_200_OK)
async def get_users(
        request: UserSearchRequest,
        user_service: UserServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.USER_READ)
):
    return await user_service.search(request)


async def