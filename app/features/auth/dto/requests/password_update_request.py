from pydantic import Field


class PasswordUpdateRequest:
    current_password: str = Field(..., min_length=12, max_length=128, description="The old password of the user")
    new_password: str = Field(..., min_length=12, max_length=128, description="The new password of the user")
