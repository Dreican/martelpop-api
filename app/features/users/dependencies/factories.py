from typing import Annotated

from fastapi import Depends

from app.features.storage.dependencies.services import StorageServiceDep
from app.features.users.factories.user_response_factory import UserResponseFactory


def get_user_response_factory() -> UserResponseFactory:
    return UserResponseFactory(storage=StorageServiceDep)


UserResponseFactoryDep = Annotated[UserResponseFactory, Depends(get_user_response_factory)]

