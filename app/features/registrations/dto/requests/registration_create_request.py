from pydantic import BaseModel, Field


class RegistrationRequest(BaseModel):
    note: str | None = Field(..., description="An optional note to include with the registration")
