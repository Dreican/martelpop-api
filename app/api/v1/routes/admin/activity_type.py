from uuid import UUID

from fastapi import APIRouter, status

from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.events.dependencies.services import ActivityTypeServiceDep
from app.features.events.dto.responses.activity_type_admin_response import ActivityTypeAdminResponse
from app.features.events.dto.responses.event_response import EventResponse

router = APIRouter(prefix="/activity_type", tags=["Admin Events"])

@router.get("/{activity_type_id}", response_model=ActivityTypeAdminResponse, status_code=status.HTTP_200_OK)
async def get_events(
        activity_type_id: UUID,
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.get_activity_type(activity_type_id)


@router.get("/{activity_type_id}/events", response_model=list[EventResponse], status_code=status.HTTP_200_OK)
async def get_events(
        activity_type_id: UUID,
        activity_type_service: ActivityTypeServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.ACTIVITY_TYPE_MANAGE)
):
    return await activity_type_service.get_events_by_activity_type(activity_type_id)

