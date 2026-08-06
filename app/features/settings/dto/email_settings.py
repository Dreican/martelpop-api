from dataclasses import dataclass


@dataclass(frozen=True)
class EmailSettings:
    enabled: bool
    support_email: str
    reply_to_email: str
    send_registration_confirmation: bool
    send_cancellation_confirmation: bool
    send_event_reminders: bool
    reminder_days_before: int
