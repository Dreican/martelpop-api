from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.features.auth.dependencies.services import PrincipalServiceDep
from app.features.auth.security.bearer import bearer_scheme
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal

CredentialsDep = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme)
]


async def get_current_principal(
        credentials: CredentialsDep,
        service: PrincipalServiceDep,
) -> Principal:
    token = (
        credentials.credentials
        if credentials is not None
        else None
    )

    return await service.authenticate(token)


CurrentPrincipalDep = Annotated[
    Principal,
    Depends(get_current_principal),
]


async def get_authenticated_principal(
        principal: CurrentPrincipalDep,
        service: PrincipalServiceDep
) -> AuthenticatedPrincipal:
    return service.require_authenticated(principal)


AuthenticatedPrincipalDep = Annotated[
    AuthenticatedPrincipal,
    Depends(get_authenticated_principal),
]
