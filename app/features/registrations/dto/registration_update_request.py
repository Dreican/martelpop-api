from uuid import UUID

from pydantic import BaseModel, Field


class RegistrationUpdateRequest(BaseModel):
    registration_id: UUID = Field(..., description="The ID of the registration to update")
    note: str = Field(..., description="The note to update the registration with")