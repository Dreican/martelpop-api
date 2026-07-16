from dataclasses import dataclass

from app.features.auth.dto.token_response import TokenResponse
from app.features.auth.models.refresh_token import RefreshToken


@dataclass(slots=True)
class AuthenticationTokens:
    response: TokenResponse
    refresh: RefreshToken
