from enum import StrEnum


class AuthProvider(StrEnum):
    LOCAL = "LOCAL"
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"
