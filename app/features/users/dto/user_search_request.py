from pydantic import BaseModel

from app.core.pagination.page_request import PageRequest
from app.features.auth.enums.role_code import RoleCode
from app.features.users.enums.user_sort import UserSort
from app.features.users.enums.user_status import UserStatus


class UserSearchRequest(BaseModel):
    pagination: PageRequest = PageRequest()

    query: str | None
    statuses: set[UserStatus] | None
    role: set[RoleCode] | None

    sort: UserSort = UserSort.CREATED_AT_DESC
