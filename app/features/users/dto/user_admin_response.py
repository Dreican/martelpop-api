from datetime import datetime

from app.features.users.dto.user_response import UserResponse


class UserAdminResponse(UserResponse):
    email: str
    firstname: str
    lastname: str
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime
