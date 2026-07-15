from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class TokenPair:
    access_token: str
    refresh_token: str

    refresh_jti: UUID
    refresh_expires_at: datetime
