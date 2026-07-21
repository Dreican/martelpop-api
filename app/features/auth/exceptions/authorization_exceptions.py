from starlette.status import HTTP_403_FORBIDDEN

from app.core.exceptions.base import ApplicationError


class PermissionDeniedError(ApplicationError):
    status_code = HTTP_403_FORBIDDEN
    code = "permission_denied"
    detail = "Permission denied"
