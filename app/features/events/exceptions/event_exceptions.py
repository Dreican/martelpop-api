from uuid import UUID

from fastapi import status
from app.core.exceptions.base import ApplicationError


class EventNotFoundError(ApplicationError):
    def __init__(self, event_id: UUID):
        detail = f"Event {event_id} not found"

    status_code = status.HTTP_404_NOT_FOUND
    code = "event_not_found"