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


class RegistrationsDisabledError(ApplicationError):
    code = "registrations_disabled"
    detail = "Registrations are disabled."


class RegistrationAlreadyCancelledError(ApplicationError):
    code = "registration_cancelled"
    detail = "Registration is already cancelled."


class RegistrationUncancelledError(ApplicationError):
    code = "registration_uncancelled"
    detail = "Registration is already uncancelled."


class RegistrationAlreadyWaitlistedError(ApplicationError):
    code = "registration_waitlisted"
    detail = "Registration is already waitlisted."


class RegistrationPromoteError(ApplicationError):
    code = "registration_promote"
    detail = "Registration promotion failed."
