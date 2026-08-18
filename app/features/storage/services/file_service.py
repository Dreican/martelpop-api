import hashlib
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.exceptions.authorization_exceptions import PermissionDeniedError
from app.features.auth.security.principal import AuthenticatedPrincipal
from app.features.storage.exceptions.storage_exceptions import StorageFileNotFoundError
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
        extension = Path(original_filename).suffix
        filename = f"{file_id}{extension}"
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
            await self._storage.save(content(), key=storage_key)

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

            await self._repository.add(stored_file)
            return stored_file

        except Exception:
            await self._storage.delete(storage_key)
            raise

    async def download(self, file_id: UUID) -> tuple[StoredFile, AsyncIterator[bytes]]:
        stored_file = await self._repository.get_required(file_id)

        if not await self._storage.exists(stored_file.storage_key):
            raise StorageFileNotFoundError(f"Storage file not found: {stored_file.storage_key}")

        content = await self._storage.read(key=stored_file.storage_key)
        return stored_file, content

    async def delete(self, file_id: UUID) -> None:
        stored_file = await self._repository.get_required(file_id)
        await self._repository.delete(stored_file)
        await self._storage.delete(stored_file.storage_key)

    async def get(self, file_id: UUID) -> StoredFile:
        return await self._repository.get_required(file_id)

    async def exists(self, file_id: UUID) -> bool:
        try:
            stored_file = await self._repository.get_required(file_id)
        except StorageFileNotFoundError:
            return False

        return await self._storage.exists(
            stored_file.storage_key,
        )

    async def verify(self, file_id: UUID) -> bool:
        stored_file = await self._repository.get(file_id)

        if not await self._storage.exists(stored_file.storage_key):
            return False

        hasher = hashlib.sha256()
        size = 0

        async for chunk in await self._storage.read(key=stored_file.storage_key):
            hasher.update(chunk)
            size += len(chunk)

        return (
            size == stored_file.size
            and hasher.hexdigest() == stored_file.checksum
        )

    async def replace(
        self,
        old_file_id: UUID | None,
        new_file: UploadFile,
        *,
        uploaded_by_id: UUID,
        category: str,
    ) -> StoredFile:
        new_stored_file = await self.upload(
            new_file,
            uploaded_by_id=uploaded_by_id,
            category=category,
        )

        if old_file_id is not None:
            await self.delete(old_file_id)

        return new_stored_file