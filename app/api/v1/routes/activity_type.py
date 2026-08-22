from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.features.auth.dependencies.require_permissions import permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import Principal
from app.features.events.dependencies.services import ActivityTypeServiceDep
from app.features.storage.helpers.content_disposition import content_disposition_inline

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
    file_download = await activity_type_service.get_icon(activity_type_slug)

    headers = {
        "Content-Disposition": content_disposition_inline(file_download.file.original_filename),
        "Content-Length": str(file_download.file.size),
        "ETag": f'"{file_download.file.checksum}"',
        "Cache-Control": (
            "public, max-age=31536000, immutable"
            if file_download.is_public
            else "private, no-cache"
        )
    }

    return StreamingResponse(
        file_download.content,
        media_type=file_download.file.mime_type,
        headers=headers
    )
