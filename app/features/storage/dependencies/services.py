from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.features.storage.dependencies.repositories import StorageRepositoryDep
from app.features.storage.services.sotrage_service import StorageService


def get_storage_service(
        session: SessionDep,
        storage_repository: StorageRepositoryDep,
) -> StorageService:
    return StorageService(
        session=session,
        storage_repository=storage_repository,
    )


StorageServiceDep = Annotated[StorageService, Depends(get_storage_service)]