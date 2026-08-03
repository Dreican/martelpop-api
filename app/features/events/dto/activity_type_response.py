from uuid import UUID

from pydantic import BaseModel


class ActivityTypeResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    name: str
    slug: str
    description: str | None
    icon_url: str | None
    color: str | None
