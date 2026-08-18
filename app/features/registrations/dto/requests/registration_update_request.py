from pydantic import BaseModel, Field


class RegistrationUpdateRequest(BaseModel):
    note: str = Field(..., description="The note to update the registration with")
