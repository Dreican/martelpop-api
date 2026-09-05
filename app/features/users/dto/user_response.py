from datetime import date, datetime

from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse
from app.features.users.enums.user_status import UserStatus


class UserResponse(UserSummaryResponse):
    email: str
    firstname: str
    lastname: str
    municipality: str | None = None
    date_of_birth: date | None = None
    role: RoleSummaryResponse
    status: UserStatus
    created_at: datetime
