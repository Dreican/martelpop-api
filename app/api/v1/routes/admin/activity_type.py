from uuid import UUID

from fastapi import APIRouter, status, UploadFile, File

from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.dependencies.services import ActivityTypeServiceDep
from app.features.events.dto.requests.activity_type_create_request import ActivityTypeCreateRequest
from app.features.events.dto.requests.activity_type_update_request import ActivityTypeUpdateRequest
from app.features.events.dto.responses.activity_type_admin_response import ActivityTypeAdminResponse
from app.features.storage.dto.stored_file_response import StoredFileResponse

router = APIRouter(prefix="/activity_type", tags=["Admin Events"])


@router.get("/{activity_type_id}", response_model=ActivityTypeAdminResponse, status_code=status.HTTP_200_OK)
async def get_activity_type(
        activity_type_id: UUID,
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.get_activity_type(activity_type_id)


@router.get("", response_model=list[ActivityTypeAdminResponse], status_code=status.HTTP_200_OK)
async def get_activity_types(
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.list_activity_type()


router.post("", response_model=ActivityTypeAdminResponse, status_code=status.HTTP_201_CREATED)


async def create_activity_type(
        request: ActivityTypeCreateRequest,
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.create_activity_type(request)


@router.put("/{activity_type_id}", response_model=ActivityTypeAdminResponse, status_code=status.HTTP_200_OK)
async def update_activity_type(
        activity_type_id: UUID,
        request: ActivityTypeUpdateRequest,
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.update_activity_type(activity_type_id, request)


@router.delete("/{activity_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity_type(
        activity_type_id: UUID,
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    await activity_type_service.delete_activity_type(activity_type_id)


@router.post("/{activity_type_id}/icon", response_model=StoredFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_event_banner(
        activity_type_id: UUID,
        activity_type_service: ActivityTypeServiceDep,
        file: UploadFile = File(...),
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.upload_icon(activity_type_id, principal, file)


@router.delete("/{activity_type_id}/icon", status_code=status.HTTP_204_NO_CONTENT)
async def remove_event_banner(
        activity_type_id: UUID,
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.delete_icon(activity_type_id)
