from app.features.events.dto.responses.activity_type_summary_response import ActivityTypeSummaryResponse


class ActivityTypeResponse(ActivityTypeSummaryResponse):
    description: str | None
    banner_url: str | None
