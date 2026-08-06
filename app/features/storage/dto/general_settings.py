from dataclasses import dataclass


@dataclass(frozen=True)
class GeneralSettings:
    application_name: str
    logo_url: str | None
    maintenance_mode: bool