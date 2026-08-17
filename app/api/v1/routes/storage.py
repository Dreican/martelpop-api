from fastapi import APIRouter, status, UploadFile, File

from app.features.auth.dependencies.current_principal import AuthenticatedPrincipalDep
from app.features.auth.dependencies.require_permissions import permission
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.storage.models.stored_file import StoredFile
from app.features.storage.services.file_service import FileService

router = APIRouter(prefix="/files", tags=["Storage"])

@router.post("", response_model=StoredFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...), service: FileService = FileService(), principal: AuthenticatedPrincipalDep) -> StoredFileResponse:
    stored_file = await service.upload(file, uploaded_by_id=principal.user.id, category="uploads")
    return stored_file
