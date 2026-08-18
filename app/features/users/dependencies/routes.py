from typing import Annotated

from fastapi import Query, Depends

from app.core.pagination.page_request import PageRequest
from app.features.auth.enums.role_code import RoleCode
from app.features.users.dto.user_search_request import UserSearchRequest
from app.features.users.enums.user_sort import UserSort
from app.features.users.enums.user_status import UserStatus


async def get_user_search_request(
    page: int = Query(1),
    page_size: int = Query(20),
    query: str | None = Query(None),
    role: set[RoleCode] | None = Query(None),
    statuses: set[UserStatus] | None = Query(None),
    sort: UserSort = Query(UserSort.CREATED_AT_DESC),
) -> UserSearchRequest:
    return UserSearchRequest(
        pagination=PageRequest(
            page=page,
            page_size=page_size,
        ),
        query=query,
        role=role,
        statuses=statuses,
        sort=sort,
    )

UserSearchRequestDep = Annotated[UserSearchRequest, Depends(get_user_search_request)]