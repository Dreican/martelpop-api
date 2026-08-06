from dataclasses import dataclass


@dataclass(frozen=True)
class GeneralSettings:
    maintenance_mode: bool
    application_url: str | None
    support_email: str | None
    contact_email: str | None
    reply_to_email: str | None