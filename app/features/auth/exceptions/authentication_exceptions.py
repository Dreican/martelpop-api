from fastapi import status

from app.core.exceptions.base import ApplicationError


class EmailAlreadyExistsError(ApplicationError):
    status_code = status.HTTP_409_CONFLICT
    code = "email_already_exists"
    detail = "Email already exists"


class InvalidCredentialsError(ApplicationError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "invalid_credentials"
    detail = "Invalid credentials"


class UserNotFoundError(ApplicationError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "user_not_found"
    detail = "User not found"


class DefaultRoleNotFoundError(ApplicationError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "default_role_not_found"
    detail = "Default role not found"


class RefreshTokenReuseDetected(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "refresh_token_reuse_detected"
    detail = "Refresh token reuse detected"
