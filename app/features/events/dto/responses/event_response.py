from app.features.events.dto.responses.activity_type_summary_response import ActivityTypeSummaryResponse
from app.features.events.dto.responses.event_status_summary_response import EventStatusSummaryResponse
from app.features.events.dto.responses.event_summary_response import EventSummaryResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class EventResponse(EventSummaryResponse):
    description: str | None

    capacity: int | None
    banner_url: str | None
    activity_type: ActivityTypeSummaryResponse
    creator: UserSummaryResponse
    status: EventStatusSummaryResponse

    is_full: bool
