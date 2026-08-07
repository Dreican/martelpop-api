from app.core.exceptions.forbidden import ForbiddenError
from app.core.exceptions.not_found import NotFoundError
from app.features.auth.enums.permission_code import PermissionCode


class PermissionNotFoundError(ForbiddenError):
    code = "permission_not_found"

    def __init__(self, permission_code: PermissionCode):
        super().__init__(f"Permission '{permission_code}' not found.", permission_code=permission_code)


class PermissionDeniedError(ForbiddenError):
    code = "permission_denied"

    def __init__(self, permissions: set[PermissionCode], user: str):
        super().__init__(f"Missing permission.", permission=permissions, user=user)


class EmailNotVerifiedError(ForbiddenError):
    code = "email_not_verified"
    detail = "Email address not verified."


class RoleLockedError(ForbiddenError):
    code = "role_locked"

    def __init__(self, role_name: str):
        super().__init__(f"Role {role_name} cannot be modified.", role_name=role_name)


class RolePermissionNotFoundError(NotFoundError):
    code = "role_permission_not_found"
    detail = "Role permission not found."