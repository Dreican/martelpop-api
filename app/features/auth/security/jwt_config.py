from dataclasses import dataclass

from pydantic import SecretStr


@dataclass(frozen=True, slots=True)
class JwtConfig:
    secret_key: SecretStr
    algorithm: str

    access_token_expiration_minutes: int
    refresh_token_expiration_days: int
