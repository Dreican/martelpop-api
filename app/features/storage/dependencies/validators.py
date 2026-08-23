from typing import Annotated

from fastapi import Depends

from app.core.config.configuration import get_config
from app.features.storage.validator.file_validator import FileValidator


def get_file_validator():
    config = get_config()
    return FileValidator(config.storage)


FileValidatorDep = Annotated[FileValidator, Depends(get_file_validator)]
