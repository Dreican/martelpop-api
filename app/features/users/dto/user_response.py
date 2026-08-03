from uuid import UUID

from pydantic import BaseModel

from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse


class UserResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    email: str
    display_name: str
    is_active: bool
    role: RoleSummaryResponse
    avatar_url: str | None
