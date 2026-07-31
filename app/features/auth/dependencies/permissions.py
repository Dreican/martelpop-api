from typing import Annotated

from fastapi import Depends

from app.features.auth.dependencies.authorization import AuthorizationServiceDep
from app.features.auth.dependencies.current_principal import CurrentPrincipal
from app.features.auth.enums.permission_code import PermissionCode


class PermissionRequirement:
    def __init__(self, *permissions: PermissionCode):
        self._permissions = set(permissions)

    async def __call__(self, principal: CurrentPrincipal, authorization: AuthorizationServiceDep) -> None:
        await authorization.require_all_permissions(principal, self._permissions)


def permission(*permissions: PermissionCode):
    return Annotated[
        None,
        Depends(PermissionRequirement(*permissions)),
    ]
