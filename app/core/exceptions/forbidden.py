from fastapi import status

from app.core.exceptions.base import ApplicationError


class ForbiddenError(ApplicationError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "permission_denied"
    detail = "Permission denied."
