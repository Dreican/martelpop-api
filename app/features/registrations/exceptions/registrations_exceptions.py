from app.core.exceptions.not_found import NotFoundError


class RegistrationNotFoundError(NotFoundError):
    code = "registration_not_found"
    detail = "Registration not found."