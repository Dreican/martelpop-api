from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config.configuration import get_config
from app.core.dependencies.database import SessionDep
from app.features.storage.dependencies.repositories import StorageRepositoryDep
from app.features.storage.dependencies.validators import FileValidatorDep
from app.features.storage.interface.storage import Storage
from app.features.storage.services.file_service import FileService
from app.features.storage.services.local_storage import LocalStorage


@lru_cache
def get_storage() -> Storage:
    config = get_config()
    return LocalStorage(
        base_path=config.storage.base_path
    )

StorageDep = Annotated[Storage, Depends(get_storage)]

def get_file_service(
        storage: StorageDep,
        storage_repository: StorageRepositoryDep,
        storage_validator: FileValidatorDep,
) -> FileService:
    return FileService(
        storage=storage,
        repository=storage_repository,
        validator=storage_validator,
    )

FileServiceDep = Annotated[FileService, Depends(get_file_service)]
