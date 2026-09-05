from uuid import UUID

from pydantic import BaseModel


class UserSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    slug: str
    display_name: str
    avatar_url: str | None = None
