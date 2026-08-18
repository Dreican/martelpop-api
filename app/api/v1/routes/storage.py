from uuid import UUID

from fastapi import APIRouter, status, UploadFile, File
from starlette.responses import StreamingResponse

from app.core.storage.file_categories import FileCategory
from app.features.auth.dependencies.require_permissions import authenticated_permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.storage.dependencies.services import FileServiceDep
from app.features.storage.dto.stored_file_response import StoredFileResponse
from app.features.storage.helpers.helpers import content_disposition_filename

router = APIRouter(prefix="/files", tags=["Storage"])


@router.post("", response_model=StoredFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(service: FileServiceDep, file: UploadFile = File(...),
                      principal: AuthenticatedPrincipal = authenticated_permission()) -> StoredFileResponse:
    stored_file = await service.upload(file, uploaded_by_id=principal.user.id, category=FileCategory.GENERAL)
    return StoredFileResponse.model_validate(stored_file)


@router.get("/{file_id}")
async def download_file(file_id: UUID, service: FileServiceDep) -> StreamingResponse:
    stored_file, content = await service.download(file_id)
    return StreamingResponse(
        content,
        media_type=stored_file.mime_type,
        headers={
            "Content-Disposition": content_disposition_filename(stored_file.original_filename),
            "Content-Length": str(stored_file.size)
        }
    )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: UUID, service: FileServiceDep,
                      principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.STORAGE_MANAGE)) -> None:
    await service.delete(file_id, principal)
