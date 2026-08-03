from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.events.dto.responses.activity_type_summary_response import ActivityTypeSummaryResponse
from app.features.events.dto.responses.event_status_summary_response import EventStatusSummaryResponse


class EventSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID
    slug: str

    title: str

    start_date: datetime | None
    end_date: datetime | None

    location: str | None
    banner_url: str | None

    activity_type: ActivityTypeSummaryResponse
    status: EventStatusSummaryResponse
