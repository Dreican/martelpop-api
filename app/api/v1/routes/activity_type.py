from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.api.v1.utils.file_response import file_stream_response
from app.features.auth.dependencies.require_permissions import permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import Principal
from app.features.events.dependencies.services import ActivityTypeServiceDep

router = APIRouter(
    prefix="/activity_type",
    tags=["Activity Type"],
)


@router.get("/{activity_type_slug}/icon")
async def get_icon(
        activity_type_slug: str,
        activity_type_service: ActivityTypeServiceDep,
        principal: Principal = permission(PermissionCode.ACTIVITY_TYPE_READ)
) -> StreamingResponse:
    download = await activity_type_service.get_icon(activity_type_slug)

    return file_stream_response(download)

@router.get("/{activity_type_slug}")
async def get_activity_type(
        activity_type_slug: str,
        activity_type_service: ActivityTypeServiceDep,
        principal: Principal = permission(PermissionCode.ACTIVITY_TYPE_READ)
) -> dict:
    activity_type = await activity_type_service.get_activity_type(activity_type_slug)

    return activity_type
