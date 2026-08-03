from uuid import UUID

from pydantic import BaseModel


class UserSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    display_name: str
    avatar_url: str | None
