import hashlib
from collections.abc import AsyncIterator
from uuid import UUID, uuid4

from fastapi import UploadFile

from app.features.storage.interface.storage import Storage
from app.features.storage.models.stored_file import StoredFile
from app.features.storage.repositories.storage_repository import StorageRepository
from app.features.storage.validator.file_validator import FileValidator


class FileService:
    CHUNK_SIZE = 1024 * 1024  # 1 MB

    def __init__(
            self,
            storage: Storage,
            repository: StorageRepository,
            validator: FileValidator
    ):
        self._storage = storage
        self._repository = repository
        self._validator = validator

    async def upload(self, file: UploadFile, *, uploaded_by_id: UUID, category: str) -> StoredFile:
        content_type = file.content_type or "application/octet-stream"

        self._validator.validate_content_type(content_type)

        file_id = uuid4()
        original_filename = file.filename or "unknown"
        filename = f"{file_id}.{original_filename.split('.')[-1]}"
        storage_key = f"{category}/{filename}"

        hasher = hashlib.sha256()
        size = 0

        async def content() -> AsyncIterator[bytes]:
            nonlocal size

            try:
                while chunk := await file.read(self.CHUNK_SIZE):
                    size += len(chunk)
                    self._validator.validate_size(size)
                    hasher.update(chunk)
                    yield chunk
            finally:
                await file.close()

        try:
            await self._storage.save(
                content(),
                key=storage_key,
            )
        except Exception:
            raise

        stored_file = StoredFile(
            id=file_id,
            filename=filename,
            original_filename=original_filename,
            storage_key=storage_key,
            mime_type=content_type,
            size=size,
            checksum=hasher.hexdigest(),
            uploaded_by_id=uploaded_by_id
        )

        await self._storage.save(content(), key=storage_key)

        try:
            await self._repository.add(stored_file)
        except Exception:
            await self._storage.delete(storage_key)
            raise

        return stored_file
