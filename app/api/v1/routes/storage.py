from uuid import UUID

from fastapi import APIRouter, status, UploadFile, File, Header, Response
from starlette.responses import StreamingResponse

from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.storage.dependencies.services import FileServiceDep
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.features.storage.enums.storage_categories import StorageCategory
from app.features.storage.helpers.helpers import content_disposition_inline, content_disposition_attachment

router = APIRouter(prefix="/files", tags=["Storage"])


@router.post("", response_model=StoredFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
        service: FileServiceDep,
        file: UploadFile = File(...),
        principal: AuthenticatedPrincipal = authenticated_permission()
) -> StoredFileResponse:
    stored_file = await service.upload(file, uploaded_by_id=principal.user.id, category=StorageCategory.GENERAL)
    return StoredFileResponse.model_validate(stored_file)


@router.get("/{file_id}/download")
async def download_file(file_id: UUID, service: FileServiceDep, principal: AuthenticatedPrincipal = authenticated_permission()) -> StreamingResponse:
    stored_file, content = await service.download(file_id)
    return StreamingResponse(
        content,
        media_type=stored_file.mime_type,
        headers={
            "Content-Disposition": content_disposition_attachment(stored_file.original_filename),
            "Content-Length": str(stored_file.size)
        }
    )

@router.get("/{file_id}")
async def get_file(file_id: UUID, service: FileServiceDep, if_none_match: str | None = Header(default=None)) -> Response:
    stored_file, content = await service.download(file_id)

    etag = f'"{stored_file.checksum}"'

    if if_none_match == etag:
        return Response(
            status_code=status.HTTP_304_NOT_MODIFIED,
            headers={"ETag": etag}
        )

    return StreamingResponse(
        content,
        media_type=stored_file.mime_type,
        headers={
            "Content-Disposition": content_disposition_inline(stored_file.original_filename),
            "Content-Length": str(stored_file.size),
            "ETag": etag,
            "Cache-Control": "public, max-age=31536000, immutable"
        }
    )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
        file_id: UUID,
        service: FileServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.STORAGE_MANAGE)
) -> None:
    await service.delete(file_id)
