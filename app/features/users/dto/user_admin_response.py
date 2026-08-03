from datetime import datetime

from app.features.users.dto.user_response import UserResponse


class UserAdminResponse(UserResponse):
    is_active: bool
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime
