from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.features.auth.enums import TokenType
from app.features.users.enums import UserRole


class TokenPayload(BaseModel):
    sub: UUID
    type: TokenType
    role: UserRole | None = None

    iss: str
    aud: str

    iat: datetime
    exp: datetime
