from app.features.events.dto.activity_type_response import ActivityTypeResponse
from app.features.events.models.activity_type import ActivityType


class ActivityTypeMapper:
    @staticmethod
    def to_response(activity_type: ActivityType) -> ActivityTypeResponse:
        return ActivityTypeResponse(
            id=activity_type.id,
            name=activity_type.name,
            description=activity_type.description,
            slug=activity_type.slug,
            icon_url=(
                f"/files/{activity_type.icon.id}"
                if activity_type.icon
                else None
            ),
            color=activity_type.color,
        )
