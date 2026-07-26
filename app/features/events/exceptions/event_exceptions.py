from typing import Any
from uuid import UUID

from fastapi import status
from app.core.exceptions.base import ApplicationError
from app.core.exceptions.not_found import NotFoundError


class EventNotFoundError(NotFoundError):
    code = "event_not_found"
    detail = "Event not found."