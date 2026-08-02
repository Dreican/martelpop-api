from app.core.exceptions.base import ApplicationError
from app.core.exceptions.not_found import NotFoundError


class RegistrationNotFoundError(NotFoundError):
    code = "registration_not_found"
    detail = "Registration not found."


class RegistrationClosedError(ApplicationError):
    code = "registration_closed"
    detail = "Registration close."


class AlreadyRegisteredError(ApplicationError):
    code = "already_registered"
    detail = "Registration already exists."


class EventFullError(ApplicationError):
    code = "event_full"
    detail = "Event is full."