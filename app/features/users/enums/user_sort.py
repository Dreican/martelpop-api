from enum import StrEnum


class UserSort(StrEnum):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"

    FULLNAME_ASC = "fullname_asc"
    FULLNAME_DESC = "fullname_desc"

    EMAIL_ASC = "email_asc"
    EMAIL_DESC = "email_desc"

    DISPLAY_NAME_ASC = "display_name_asc"
    DISPLAY_NAME_DESC = "display_name_desc"

    ROLE_ASC = "role_asc"
    ROLE_DESC = "role_desc"

    STATUS_ASC = "status_asc"
    STATUS_DESC = "status_desc"