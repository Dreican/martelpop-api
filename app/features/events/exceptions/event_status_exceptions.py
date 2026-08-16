from fastapi import status

from app.core.exceptions.base import ApplicationError
from app.core.exceptions.not_found import NotFoundError


class DefaultEventStatusNotFoundError(ApplicationError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "default_event_status_not_found"
    detail = "Default event status not found"


class EventStatusNotFoundError(NotFoundError):
    code = "event_status_not_found"
    detail = "Event status not found"
