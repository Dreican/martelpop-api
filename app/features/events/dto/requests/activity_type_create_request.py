from pydantic import BaseModel, Field


class ActivityTypeCreateRequest(BaseModel):
    name: str = Field(..., description="The name of the activity type")
    description: str | None = Field(..., description="The description of the event")
    color: str | None  = Field(..., description="The color of the activity type")
    default_location: str | None  = Field(..., description="The default location of the activity type")
    default_capacity: int | None  = Field(..., description="The default capacity of the activity type")
    default_duration_minutes: int | None  = Field(..., description="The default duration of the activity type in minutes")
