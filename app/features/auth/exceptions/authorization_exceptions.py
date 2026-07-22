from fastapi import status

from app.core.exceptions.base import ApplicationError
from app.features.auth.enums.permission_code import PermissionCode


class ForbiddenException(ApplicationError):
    status_code = status.HTTP_403_FORBIDDEN


class PermissionDeniedError(ForbiddenException):
    code = "permission_denied"

    def __init__(self, permission: set[PermissionCode]):
        self.detail = f"Missing permission '{permission}'."


class EmailNotVerifiedError(ForbiddenException):
    code = "email_not_verified"

    def __init__(self):
        super().__init__(f"Email address not verified.")


class RoleLockedError(ForbiddenException):
    code = "role_locked"

    def __init__(self, role_name: str):
        super().__init__(f"Role {role_name} cannot be modified.")
