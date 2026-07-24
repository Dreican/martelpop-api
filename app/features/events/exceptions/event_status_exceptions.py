from fastapi import status
from app.core.exceptions.base import ApplicationError


class DefaultEventStatusNotFoundError(ApplicationError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "default_event_status_not_found"
    detail = "Default event status not found"