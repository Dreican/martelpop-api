from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.repositories.base_repository import BaseRepository
from app.features.storage.exceptions.storage_exceptions import StorageFileNotFoundError
from app.features.storage.models.stored_file import StoredFile


class StorageRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=StoredFile, not_found_exception=StorageFileNotFoundError)
