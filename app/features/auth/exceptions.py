from app.core.exceptions.base import ApplicationError


class JwtError(Exception):
    """Base JWT exception."""


class InvalidTokenError(JwtError):
    pass


class ExpiredTokenError(JwtError):
    pass


class InvalidTokenTypeError(JwtError):
    pass


class EmailAlreadyExistsError(ApplicationError):
    status_code = 409
    code = "email_already_exists"
    detail = "Email already exists"


class InvalidCredentialsError(ApplicationError):
    status_code = 401
    code = "invalid_credentials"
    detail = "Invalid credentials"


class UserNotFoundError(ApplicationError):
    status_code = 404
    code = "user_not_found"
    detail = "User not found"


class DefaultRoleNotFoundError(ApplicationError):
    status_code = 500
    code = "default_role_not_found"
    detail = "Default role not found"


class RefreshTokenReuseDetected(ApplicationError):
    status_code = 400
    code = "refresh_token_reuse_detected"
    detail = "Refresh token reuse detected"
