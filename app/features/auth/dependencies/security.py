from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer(
    auto_error=False,
)

credential: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]