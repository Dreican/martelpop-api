from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "MartelPop API"

    DEBUG: bool = False

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    DATABASE_URL: str

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
