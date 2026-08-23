from app.core.config.storage import StorageConfig
from app.features.storage.exceptions.storage_exceptions import FileTooLargeError, InvalidFileTypeError


class FileValidator:

    def __init__(self, storage_config: StorageConfig):
        self._storage_config = storage_config

    def validate_content_type(self, content_type: str) -> None:
        if content_type not in self._storage_config.allowed_content_types:
            raise InvalidFileTypeError(f"Invalid content type: {content_type}")

    def validate_size(self, size: int) -> None:
        if size > self._storage_config.max_upload_size:
            raise FileTooLargeError(
                f"File size exceeds the limit: "f"{size / 1024 / 1024:.2f} MB"
            )
