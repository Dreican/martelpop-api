from fastapi import status

from app.core.exceptions.base import ApplicationError


class UnauthorizedError(ApplicationError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "unauthorized"
    detail = "Authentication required."


class InvalidTokenError(UnauthorizedError):
    code = "invalid_token"
    detail = "Invalid token."


class ExpiredTokenError(UnauthorizedError):
    code = "expired_token"
    detail = "Expired token."


class InvalidTokenTypeError(UnauthorizedError):
    code = "invalid_token_type"
    detail = "Invalid token type."
