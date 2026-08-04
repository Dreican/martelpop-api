from uuid import UUID

from pydantic import BaseModel

from app.core.pagination.page_request import PageRequest
from app.features.registrations.enums.registration_sort import RegistrationSort
from app.features.registrations.enums.registration_status import RegistrationStatus


class RegistrationParticipantRequest(BaseModel):
    pagination: PageRequest = PageRequest()

    event_id: UUID
    statuses: set[RegistrationStatus] | None
    include_cancelled: bool = True

    page: int = 1
    page_size: int = 20

    sort: RegistrationSort = RegistrationSort.REGISTRATION_DATE_DESC