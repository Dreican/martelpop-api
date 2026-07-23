from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.events.dto.activity_type_response import ActivityTypeResponse
from app.features.events.dto.event_status_response import EventStatusResponse
from app.features.users.dto.user_response import UserResponse


class EventResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    title: str
    description: str | None
    slug: str
    location: str | None
    banner_url: str | None
    start_date: datetime | None
    end_date: datetime | None
    capacity: int | None
    activity_type_id: ActivityTypeResponse
    creator: UserResponse
    status: EventStatusResponse
