from typing import Annotated

from fastapi import Depends

from app.core.config.configuration import Configuration, get_config

ConfigDep = Annotated[Configuration, Depends(get_config)]
