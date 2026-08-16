from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.core.dependencies.response_factories import UserResponseFactoryDep, UserAdminResponseFactoryDep
from app.core.dependencies.slug import SlugServiceDep
from app.features.auth.dependencies.repositories import RoleRepositoryDep
from app.features.users.dependencies.repositories import UserRepositoryDep
from app.features.users.factories.user_admin_response_factory import UserAdminResponseFactory
from app.features.users.services.user_services import UserService


def get_user_service(
        session: SessionDep,
        user_repository: UserRepositoryDep,
        role_repository: RoleRepositoryDep,
        slug_service: SlugServiceDep,
        user_response: UserResponseFactoryDep,
        user_admin_response: UserAdminResponseFactoryDep
) -> UserService:
    return UserService(
        session=session,
        user_repository=user_repository,
        role_repository=role_repository,
        slug_service=slug_service,
        user_response=user_response,
        user_admin_response=user_admin_response,
    )

UserServiceDep = Annotated[UserService, Depends(get_user_service)]