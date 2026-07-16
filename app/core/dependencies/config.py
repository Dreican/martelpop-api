from typing import Annotated

from anyio.functools import lru_cache
from fastapi import Depends

from app.core.config.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
