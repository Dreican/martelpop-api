from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.base_service import BaseService
from app.features.storage.repositories.storage_repository import StorageRepository


class StorageService(BaseService):
    def __init__(
            self,
            session: AsyncSession,
            storage_repository: StorageRepository
    ):
        super().__init__(session)
        self.storage_repository = storage_repository


    @staticmethod
    def public_url(file_id: UUID | None) -> str | None:
        if file_id is None:
            return None

        return f"https://api.martelpop.com/storage/{file_id}"