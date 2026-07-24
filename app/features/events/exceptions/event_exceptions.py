from uuid import UUID

from fastapi import status
from app.core.exceptions.base import ApplicationError


class EventNotFoundError(ApplicationError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "event_not_found"
    detail = "Event not found."