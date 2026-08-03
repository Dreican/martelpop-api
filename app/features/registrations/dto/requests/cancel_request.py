from uuid import UUID

from pydantic import BaseModel, Field


class CancelRequest(BaseModel):
    registration_id: UUID = Field(..., description="The ID of the registration to cancel")
    event_id: UUID = Field(..., description="The ID of the event to register for")
    note: str | None = Field(..., description="An optional note to include with the registration")
