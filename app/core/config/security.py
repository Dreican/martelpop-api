from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JWT_", extra="ignore")

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expiration_minutes: int = 15
    refresh_token_expiration_days: int = 30