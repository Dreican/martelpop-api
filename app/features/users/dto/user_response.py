from uuid import UUID

from pydantic import BaseModel

from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class UserResponse(UserSummaryResponse):
    email: str
    is_active: bool
    role: RoleSummaryResponse
