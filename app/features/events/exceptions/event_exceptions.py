from app.core.exceptions.not_found import NotFoundError


class EventNotFoundError(NotFoundError):
    code = "event_not_found"
    detail = "Event not found."