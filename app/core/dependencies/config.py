from typing import Annotated

from anyio.functools import lru_cache
from fastapi import Depends

from app.core.config.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_jwt_config(config: Config):
    return config.jwt


Config = Annotated[Settings, Depends(get_settings)]
JwtConfig = Annotated[Settings.jwt, Depends(get_jwt_config)]
