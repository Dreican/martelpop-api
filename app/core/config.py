from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "MartelPop API"

    DEBUG: bool = False

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: str = "application.log"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
