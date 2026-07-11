class JwtError(Exception):
    """Base JWT exception."""


class InvalidTokenError(JwtError):
    pass


class ExpiredTokenError(JwtError):
    pass


class InvalidTokenTypeError(JwtError):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class DefaultRoleNotFoundError(Exception):
    pass