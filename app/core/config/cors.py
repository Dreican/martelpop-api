from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class CORSSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="CORS_",
    )

    backend_cors_origins: list[str] = []
