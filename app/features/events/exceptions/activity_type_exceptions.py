from fastapi import status

from app.core.exceptions.base import ApplicationError


class ActivityTypeNotFoundError(ApplicationError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "activity_type_not_found"
    detail = "Activity type not found"
