from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.auth.enums.role_code import RoleCode
from app.features.auth.enums.token_type import TokenType


class TokenPayload(BaseModel):
    sub: UUID
    type: TokenType
    role: RoleCode | None = None

    iss: str
    aud: str

    iat: datetime
    exp: datetime
    jti: UUID
    nbf: datetime
