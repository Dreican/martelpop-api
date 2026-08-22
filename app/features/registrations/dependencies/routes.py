from typing import Annotated

from fastapi import Depends, Query

from app.core.pagination.page_request import PageRequest
from app.features.registrations.dto.requests.registration_search_request import RegistrationSearchRequest
from app.features.registrations.enums.registration_sort import RegistrationSort
from app.features.registrations.enums.registration_status import RegistrationStatus


async def get_registration_search_request(
        page: int = Query(1),
        page_size: int = Query(20),
        statuses: set[RegistrationStatus] | None = Query(None),
        sort: RegistrationSort = Query(RegistrationSort.REGISTRATION_DATE_DESC),
) -> RegistrationSearchRequest:
    return RegistrationSearchRequest(
        pagination=PageRequest(
            page=page,
            page_size=page_size,
        ),
        statuses=statuses,
        sort=sort,
    )


RegistrationSearchRequestDep = Annotated[RegistrationSearchRequest, Depends(get_registration_search_request)]
