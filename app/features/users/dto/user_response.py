from uuid import UUID

from pydantic import BaseModel

from app.features.users.dto.role_response import RoleResponse


class UserResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    email: str
    firstname: str
    lastname: str
    is_active: bool
    role: RoleResponse
    avatar_url: str | None
