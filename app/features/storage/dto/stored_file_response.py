from uuid import UUID

from pydantic import BaseModel


class StoredFileResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    url: str
