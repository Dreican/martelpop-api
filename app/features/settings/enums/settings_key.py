from enum import StrEnum


class SettingsKey(StrEnum):
    APPLICATION_NAME = "application_name"

    APPLICATION_LOGO = "application_logo"

    APPLICATION_SUPPORT_EMAIL = "application_support_email"

    APPLICATION_URL = "application_url"

    DEFAULT_PAGE_SIZE = "default_page_size"

    MAX_PAGE_SIZE = "max_page_size"

    DEFAULT_EVENT_LOCATION = "default_event_location"

    DEFAULT_EVENT_CAPACITY = "default_event_capacity"

    REGISTRATIONS_ENABLED = "registrations_enabled"

    MAINTENANCE_MODE = "Maintenance_mode"