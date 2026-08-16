from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.features.storage.repositories.storage_repository import StorageRepository


def get_storage_repository(session: SessionDep) -> StorageRepository:
    return StorageRepository(session=session)


StorageRepositoryDep = Annotated[StorageRepository, Depends(get_storage_repository)]
