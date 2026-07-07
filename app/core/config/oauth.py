from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class OAuthSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="OAUTH_",
    )

    google_client_id: str
    google_client_secret: SecretStr

    facebook_client_id: str
    facebook_client_secret: SecretStr

    frontend_url: str = "http://localhost:5173"
