from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.features.storage.enums.storage_categories import StorageCategory


class StoredFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    original_filename: str
    mime_type: str
    size: int
    category: StorageCategory
    url: str | None