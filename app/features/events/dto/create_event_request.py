from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateEventRequest(BaseModel):
    title: str = Field(..., description="The title of the event")
    slug: str = Field(..., description="The slug of the event")
    description: str | None = Field(..., description="The description of the event")
    activity_type_id: UUID = Field(..., description="The ID of the activity type")
    location: str = Field(..., description="The location of the event")
    starts_at: datetime = Field(..., description="The start time of the event")
    ends_at: datetime = Field(..., description="The end time of the event")
    capacity: int | None = Field(..., description="The capacity of the event")
