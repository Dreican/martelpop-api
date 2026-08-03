from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.events.dto.responses.event_response import EventResponse
from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.users.dto.user_response import UserResponse


class RegistrationResponse(BaseModel):
    model_config = dict(from_attributes=True)

    id: UUID
    event: EventResponse
    user: UserResponse
    note: str
    registered_at: datetime
    status: RegistrationStatus
