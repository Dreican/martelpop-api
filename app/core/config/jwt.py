from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class JWTSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="JWT_",
    )

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expiration_minutes: int = 15
    refresh_token_expiration_days: int = 30
