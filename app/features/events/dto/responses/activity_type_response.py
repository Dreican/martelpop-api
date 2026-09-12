from app.features.events.dto.responses.activity_type_summary_response import ActivityTypeSummaryResponse


class ActivityTypeResponse(ActivityTypeSummaryResponse):
    description: str | None
    banner_url: str | None
    default_location: str | None
    default_capacity: int | None
    default_duration_minutes: int | None
    default_price: int | None
