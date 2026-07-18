from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.features.users.repositories.user_repository import UserRepository


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
