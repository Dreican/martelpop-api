from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.registrations.enums.registration_status import RegistrationStatus
from app.features.users.dto.user_summary_response import UserSummaryResponse


class ParticipantResponse(BaseModel):
    model_config = dict(from_attributes=True)
    id: UUID

    user: UserSummaryResponse
    status: RegistrationStatus

    note: str

    registered_at: datetime
