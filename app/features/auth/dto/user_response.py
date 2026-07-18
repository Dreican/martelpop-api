from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    email: str
    firstname: str
    lastname: str
    is_active: bool
    role: str
    avatar_url: str | None
