from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.auth.enums.token_type import TokenType
from app.features.users.enums.user_role import UserRole


class TokenPayload(BaseModel):
    sub: UUID
    type: TokenType
    role: UserRole | None = None

    iss: str
    aud: str

    iat: datetime
    exp: datetime
    jti: UUID | None = None
    nbf: datetime
