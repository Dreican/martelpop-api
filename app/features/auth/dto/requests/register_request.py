from datetime import date

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    firstname: str = Field(..., min_length=1, max_length=100, description="The first name of the user")
    lastname: str = Field(..., min_length=1, max_length=100, description="The last name of the user")
    display_name: str = Field(..., min_length=1, max_length=100, description="The display name of the user")
    password: str = Field(..., min_length=12, max_length=128, description="The password of the user")
    municipality: str | None = Field(None, max_length=100, description="The user's municipality")
    date_of_birth: date | None = Field(None, description="The user's date of birth")
