from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class BrandingSettings:
    application_name: str | None
    logo_file_id: UUID | None
    favicon_file_id: UUID | None
    footer_text: str | None
