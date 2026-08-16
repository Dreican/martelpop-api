from datetime import datetime

from app.features.events.dto.responses.event_response import EventResponse
from app.features.events.dto.responses.event_status_response import EventStatusResponse
from app.features.events.enums.event_audience import EventAudience


class EventAdminResponse(EventResponse):
    status: EventStatusResponse

    audience: EventAudience

    published_at: datetime | None
    cancelled_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
