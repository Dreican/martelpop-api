from pydantic import Field
from pydantic.v1 import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings

from .app import AppConfig
from .cors import CORSConfig
from .database import DatabaseConfig
from .jwt import JWTConfig
from .logging import LogConfig
from .oauth import OAuthConfig
from .smtp import SMTPConfig
from .storage import StorageConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
    )

    app: AppConfig = Field(default_factory=AppConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    smtp: SMTPConfig = Field(default_factory=SMTPConfig)
    cors: CORSConfig = Field(default_factory=CORSConfig)
    log: LogConfig = Field(default_factory=LogConfig)
    oauth: OAuthConfig = Field(default_factory=OAuthConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
