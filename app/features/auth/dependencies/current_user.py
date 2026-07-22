from typing import Annotated, NoReturn

from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials

from app.features.auth.dependencies.services import JwtServiceDep
from app.features.auth.exceptions.jwt_exceptions import InvalidTokenError, ExpiredTokenError
from app.features.auth.security.bearer import bearer_scheme
from app.features.users.dependencies.repositories import UserRepositoryDep
from app.features.users.models.user import User

Credentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme)
]


def unauthorized(detail: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(credentials: Credentials, jwt: JwtServiceDep, users: UserRepositoryDep) -> User:
    if credentials is None:
        unauthorized("Not Authenticated")

    try:
        payload = jwt.decode_access_token(str(credentials.credentials))

    except ExpiredTokenError:
        unauthorized("Access token expired")

    except InvalidTokenError:
        unauthorized("Invalid access token")

    user = await users.get_by_id(payload.sub)

    if user is None:
        unauthorized("User not found")

    assert user is not None

    if not user.is_active:
        unauthorized("User account is disabled")

    if user.is_deleted:
        unauthorized("User not found")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
