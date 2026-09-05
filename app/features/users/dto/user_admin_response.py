from datetime import datetime

from app.features.users.dto.user_response import UserResponse


class UserAdminResponse(UserResponse):
    deleted_at: datetime | None
    updated_at: datetime
