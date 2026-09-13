from app.features.events.dto.responses.event_summary_response import EventSummaryResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class EventResponse(EventSummaryResponse):
    description: str | None

    location: str | None
    banner_url: str | None
    capacity: int | None
    price: float | None

    creator: UserSummaryResponse

    is_full: bool
