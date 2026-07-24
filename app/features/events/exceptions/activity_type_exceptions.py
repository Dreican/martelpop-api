from fastapi import status

from app.core.exceptions.base import ApplicationError


class ActivityTypeNotFoundError(ApplicationError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "activity_type_not_found"
    detail = "Activity type not found"
