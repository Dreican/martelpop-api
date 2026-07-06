from pydantic import computed_field
from pydantic_settings import BaseSettings

from app.core.config.security import JwtSettings


class Settings(BaseSettings):
    jwt: JwtSettings = JwtSettings()

    APP_NAME: str = "MartelPop API"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "DEV"
    HOST: str = "localhost"
    PORT: int = 8000

    DEBUG: bool = False

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: str = "application.log"

    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "martelpop"
    DB_USER: str = "martelpop"
    DB_PASSWORD: str = "martelpop"

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str

    FRONTEND_URL: str = "http://localhost:8100"

    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760
    ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]

    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM: str = "noreply@martelpop.dev"

    BACKEND_CORS_ORIGINS: list[str] = []

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
