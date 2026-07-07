from pydantic import computed_field
from pydantic_settings import SettingsConfigDict

from app.core.config.base import AppBaseSettings


class DatabaseSettings(AppBaseSettings):
    model_config = SettingsConfigDict(
        **AppBaseSettings.model_config,
        env_prefix="DB_",
    )

    host: str = "db"
    port: int = 5432
    name: str = "martelpop"
    user: str = "martelpop"
    password: str = "martelpop"

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
