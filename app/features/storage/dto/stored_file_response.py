from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StoredFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    original_filename: str
    mime_type: str
    size: int
    checksum: str
