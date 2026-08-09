from pydantic import BaseModel, Field


class UserUpdateRequest(BaseModel):
    email: str = Field(..., description="The user's email address")
    display_name: str = Field(..., description="The user's display name")
    firstname: str = Field(..., description="The user's first name")
    lastname: str = Field(..., description="The user's last name")

