from app.features.events.dto.responses.activity_type_response import ActivityTypeResponse


class ActivityTypeAdminResponse(ActivityTypeResponse):
    default_location: str | None
    default_capacity: int | None
    default_duration_minutes: int | None
    is_default: bool
