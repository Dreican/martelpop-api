from datetime import date

from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class UserResponse(UserSummaryResponse):
    is_active: bool
    email: str
    firstname: str
    lastname: str
    municipality: str | None
    date_of_birth: date | None
    role: RoleSummaryResponse
