from uuid import UUID

from pydantic import BaseModel


class StoredFileResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    filename: str
    mime_type: str
    storage_path: str
