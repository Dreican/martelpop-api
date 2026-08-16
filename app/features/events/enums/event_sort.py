from enum import StrEnum


class EventSort(StrEnum):
    START_DATE_ASC = "start_date_asc"
    START_DATE_DESC = "start_date_desc"

    END_DATE_ASC = "end_date_asc"
    END_DATE_DESC = "end_date_desc"

    CREATE_DATE_ASC = "create_date_asc"
    CREATE_DATE_DESC = "create_date_desc"

    TITLE_ASC = "title_asc"
    TITLE_DESC = "title_desc"
