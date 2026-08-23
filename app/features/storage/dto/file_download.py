from collections.abc import AsyncIterator
from dataclasses import dataclass

from app.features.storage.models.stored_file import StoredFile


@dataclass(frozen=True)
class FileDownload:
    file: StoredFile
    content: AsyncIterator[bytes]
    is_public: bool
