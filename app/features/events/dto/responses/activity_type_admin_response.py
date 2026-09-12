from datetime import datetime

from app.features.events.dto.responses.activity_type_response import ActivityTypeResponse
from app.features.users.dto.user_summary_response import UserSummaryResponse


class ActivityTypeAdminResponse(ActivityTypeResponse):
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    deleted_by: UserSummaryResponse
    is_default: bool
