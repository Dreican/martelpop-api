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



    def to_jwt_payload(self) -> dict:
        payload = self.model_dump(mode="json")

        payload["sub"] = str(self.sub)
        payload["jti"] = str(self.jti)
        payload["iat"] = int(self.iat.timestamp())
        payload["exp"] = int(self.exp.timestamp())
        payload["nbf"] = int(self.nbf.timestamp())

        return payload