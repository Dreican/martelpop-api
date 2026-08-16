from pydantic import BaseModel

from app.core.pagination.page_request import PageRequest
from app.features.registrations.enums.registration_sort import RegistrationSort
from app.features.registrations.enums.registration_status import RegistrationStatus


class RegistrationSearchRequest(BaseModel):
    pagination: PageRequest = PageRequest()

    statuses: set[RegistrationStatus] | None

    sort: RegistrationSort = RegistrationSort.REGISTRATION_DATE_DESC
