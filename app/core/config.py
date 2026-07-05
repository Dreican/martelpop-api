from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "MartelPop API"

    DEBUG: bool = False

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"


settings = Settings()
