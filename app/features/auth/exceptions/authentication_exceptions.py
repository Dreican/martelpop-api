from fastapi import status

from app.core.exceptions.base import ApplicationError
from app.core.exceptions.not_found import NotFoundError


class EmailAlreadyExistsError(ApplicationError):
    status_code = status.HTTP_409_CONFLICT
    code = "email_already_exists"
    detail = "Email already exists"


class InvalidCredentialsError(ApplicationError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "invalid_credentials"
    detail = "Invalid credentials"


class RoleNotFoundError(NotFoundError):
    code = "role_not_found"
    detail = "Role not found"


class DefaultRoleNotFoundError(ApplicationError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "default_role_not_found"
    detail = "Default role not found"


class RefreshTokenReuseDetected(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "refresh_token_reuse_detected"
    detail = "Refresh token reuse detected"


class AuthenticationIdentityNotFoundError(NotFoundError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "authentication_identity_not_found"
    detail = "Authentication identity not found"


class RefreshTokenNotFoundError(NotFoundError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "refresh_token_not_found"
    detail = "Refresh token not found"


class PasswordPolicyError(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "password_policy_violation"
    detail = "Password policy violation"