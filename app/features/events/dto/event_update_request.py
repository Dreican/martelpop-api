from datetime import datetime

from pydantic import BaseModel, Field


class EventUpdateRequest(BaseModel):
    title: str = Field(..., description="The title of the event")
    description: str = Field(..., description="The description of the event")
    location: str = Field(..., description="The location of the event")
    start_at: datetime = Field(..., description="The start time of the event")
    end_at: datetime = Field(..., description="The end time of the event")
    capacity: int = Field(..., description="The capacity of the event")