from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials

from app.features.auth.dependencies.services import JwtServiceDep
from app.features.auth.exceptions import ExpiredTokenError, InvalidTokenError
from app.features.auth.security.bearer import bearer_scheme
from app.features.users.dependencies.repositories import UserRepositoryDep
from app.features.users.models.user import User

Credentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme)
]


async def get_current_user(credentials: Credentials, jwt: JwtServiceDep, users: UserRepositoryDep) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated")

    try:
        payload = jwt.decode_access_token(credentials.credentials)

    except ExpiredTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired")

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    user = await users.get_by_id(payload.sub)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
