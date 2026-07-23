from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING_EMAIL_VERIFICATION = "PENDING_EMAIL_VERIFICATION"
