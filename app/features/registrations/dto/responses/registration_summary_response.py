from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.registrations.enums.registration_status import RegistrationStatus


class RegistrationSummaryResponse(BaseModel):
    model_config = dict(from_attributes=True)

    id: UUID
    registered_at: datetime
    status: RegistrationStatus
