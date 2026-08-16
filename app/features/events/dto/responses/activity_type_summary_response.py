from uuid import UUID

from pydantic import BaseModel


class ActivityTypeSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    name: str
    slug: str
    icon_url: str | None
