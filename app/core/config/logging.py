from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class LogSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="LOG_",
    )

    level: str = "INFO"
    dir: str = "/code/logs"
    file: str = "application.log"
