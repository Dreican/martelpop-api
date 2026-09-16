from datetime import datetime

from app.features.users.dto.user_response import UserResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class UserAdminResponse(UserResponse):
    deleted_at: datetime | None
    deleted_by: UserSummaryResponse | None
    updated_at: datetime
