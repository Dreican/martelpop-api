class JwtError(Exception):
    """Base JWT exception."""


class InvalidTokenError(JwtError):
    pass


class ExpiredTokenError(JwtError):
    pass


class InvalidTokenTypeError(JwtError):
    pass
