from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    firstname: str = Field(..., min_length=1, max_length=100, description="The first name of the user")
    lastname: str = Field(..., min_length=1, max_length=100, description="The last name of the user")
    password: str = Field(...,  min_length=10, max_length=255, description="The password of the user")