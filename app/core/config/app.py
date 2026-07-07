from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class AppSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="APP_",
    )

    name: str = "MartelPop API"
    version: str = "0.1.0"
    env: str = "DEV"
    host: str = "localhost"
    port: int = 8000
    api_prefix: str = "/api/v1"
    debug: bool = False
