from app.features.events.dto.responses.event_status_summary_response import EventStatusSummaryResponse


class EventStatusResponse(EventStatusSummaryResponse):
    description: str | None
    is_default: bool
    sort_order: int
    is_bookable: bool
    allow_edit: bool
