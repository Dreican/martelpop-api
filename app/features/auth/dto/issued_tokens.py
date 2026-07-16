from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.features.auth.dto.token_response import TokenResponse


@dataclass(slots=True)
class IssuedTokens:
    access_token: str
    refresh_token: str

    refresh_jti: UUID
    refresh_expires_at: datetime

    def to_response(self) -> TokenResponse:
        return TokenResponse(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            token_type="bearer",
        )
