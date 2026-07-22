from typing import Annotated

from fastapi import Depends

from app.features.auth.dependencies.authorization import AuthorizationServiceDep
from app.features.auth.dependencies.current_user import CurrentUser
from app.features.auth.enums.permission_code import PermissionCode


class RequirePermission:
    def __init__(self, *permissions: PermissionCode):
        self._permissions = set(permissions)

    async def __call__(self, user: CurrentUser, authorization: AuthorizationServiceDep) -> None:
        await authorization.require_all_permissions(user, self._permissions)


def Permission(*permissions: PermissionCode):
    return Annotated[
        None,
        Depends(RequirePermission(*permissions)),
    ]
