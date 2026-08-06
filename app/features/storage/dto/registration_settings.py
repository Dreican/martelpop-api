from dataclasses import dataclass


@dataclass(frozen=True)
class RegistrationSettings:
    registrations_enabled: bool
    waitlist_enabled: bool
    open_days_before: int
    close_hours_before: int