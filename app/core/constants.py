from uuid import UUID

SYSTEM_USER_ID = UUID("00000000-0000-0000-0000-000000000001")

class ErrorCode:
    VALIDATION_ERROR = "validation_error"
    INTERNAL_VALIDATION_ERROR = "internal_validation_error"
    INTERNAL_SERVER_ERROR = "internal_server_error"

