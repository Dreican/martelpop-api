from enum import StrEnum


class SettingsKey(StrEnum):
    MAINTENANCE_MODE = "maintenance_mode"
    APPLICATION_URL = "application_url"
    REPLY_TO_EMAIL = "email_reply_to"
    SUPPORT_EMAIL = "support_email"
    CONTACT_EMAIL = "contact_email"


    APPLICATION_NAME = "application_name"
    APPLICATION_LOGO = "application_logo"
    APPLICATION_FAVICON = "application_favicon"
    FOOTER_TEXT = "footer_text"

    DEFAULT_PAGE_SIZE = "default_page_size"
    MAX_PAGE_SIZE = "max_page_size"

    DEFAULT_EVENT_LOCATION = "default_event_location"
    DEFAULT_EVENT_CAPACITY = "default_event_capacity"
    DEFAULT_EVENT_DURATION = "default_event_duration"

    REGISTRATIONS_ENABLED = "registrations_enabled"
    WAITLIST_ENABLED = "waitlist_enabled"
    OPEN_DAYS_BEFORE = "open_days_before"
    CLOSE_HOURS_BEFORE = "close_hours_before"

    EMAIL_ENABLE = "email_enable"
    EMAIL_SUPPORT_ADDRESS = "email_support_address"
    EMAIL_SEND_REGISTRATION_CONFIRMATION = "email_send_registration_confirmation"
    EMAIL_SEND_CANCELLATION_CONFIRMATION = "email_send_cancellation_confirmation"
    EMAIL_SEND_EVENT_REMINDERS = "email_send_event_reminders"
    EMAIL_REMINDER_DAYS_BEFORE = "email_reminder_days_before"
