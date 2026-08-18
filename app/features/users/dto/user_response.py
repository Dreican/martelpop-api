from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class UserResponse(UserSummaryResponse):
    is_active: bool
    role: RoleSummaryResponse
