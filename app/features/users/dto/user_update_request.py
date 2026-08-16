from uuid import UUID

from pydantic import BaseModel, Field

from app.features.users.enums.user_status import UserStatus


class UserUpdateRequest(BaseModel):
    email: str = Field(..., description="The user's email address")
    display_name: str = Field(..., description="The user's display name")
    firstname: str = Field(..., description="The user's first name")
    lastname: str = Field(..., description="The user's last name")
    status: UserStatus = Field(..., description="The user's status")


