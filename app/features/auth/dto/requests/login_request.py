from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., min_length=12, max_length=128, description="The password of the user")
