from enum import StrEnum


class RegistrationSort(StrEnum):
    REGISTRATION_DATE_ASC = "registration_date_asc"
    REGISTRATION_DATE_DESC = "registration_date_desc"

    CANCELLED_REGISTRATION_DATE_ASC = "cancelled_registration_date_asc"
    CANCELLED_REGISTRATION_DATE_DESC = "cancelled_registration_desc"

    REGISTRATION_STATUS_ASC = "registration_status_asc"
    REGISTRATION_STATUS_DESC = "registration_status_desc"