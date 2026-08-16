from fastapi import status

from app.core.exceptions.base import ApplicationError


class NotFoundError(ApplicationError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    detail = "Resource not found."
