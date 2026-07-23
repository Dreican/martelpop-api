from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.events.enums.event_status_code import EventStatusCode


class CreateEventRequest(BaseModel):
    title: str
    slug: str
    description: str
    activity_type_id: UUID
    location: str
    starts_at: datetime
    ends_at: datetime
    capacity: int
    status: EventStatusCode
