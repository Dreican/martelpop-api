from dataclasses import dataclass


@dataclass(frozen=True)
class EmailSettings:
    enabled: bool
    send_registration_confirmation: bool
    send_cancellation_confirmation: bool
    send_event_reminders: bool
    reminder_days_before: int
