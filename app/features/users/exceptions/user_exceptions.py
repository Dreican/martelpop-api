from starlette import status

from app.core.exceptions.base import ApplicationError
from app.core.exceptions.forbidden import ForbiddenError


class UserNotFoundError(ApplicationError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "user_not_found"
    detail = "User not found"


class UserInactiveError(ForbiddenError):
    code = "user_inactive"
    detail = "User is inactive"
