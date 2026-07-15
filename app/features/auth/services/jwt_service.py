from datetime import datetime, UTC
from uuid import UUID, uuid4

import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError as PyJwtError

from app.core.config.jwt import JWTConfig
from app.features.auth.dto.token_pair import TokenPair
from app.features.auth.enums.token_type import TokenType
from app.features.auth.exceptions import (
    ExpiredTokenError,
    InvalidTokenError, InvalidTokenTypeError,
)
from app.features.auth.models.role import Role
from app.features.auth.security.token_payload import TokenPayload
from app.features.users.models.user import User


class JwtService:

    def __init__(self, config: JWTConfig):
        self._config = config

    @property
    def _signing_key(self) -> str:
        return self._config.secret_key.get_secret_value()

    def _create_token(self, *, user_id: UUID,
                      token_type: TokenType,
                      issued_at: datetime,
                      expires_at: datetime,
                      jti: UUID,
                      role: Role | None = None) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "type": token_type.value,
            "iat": issued_at,
            "exp": expires_at,
            "iss": self._config.issuer,
            "aud": self._config.audience,
            "nbf": issued_at,
            "jti": jti,
        }

        if role is not None:
            payload["role"] = role.name

        return jwt.encode(payload, self._signing_key, algorithm=self._config.algorithm)

    def _decode(self, token: str, expected_type: TokenType) -> TokenPayload:
        try:
            decoded = jwt.decode(
                token,
                self._signing_key,
                algorithms=[self._config.algorithm],
                issuer=self._config.issuer,
                audience=self._config.audience,
            )

            payload = TokenPayload.model_validate(decoded)

            if payload.type != expected_type:
                raise InvalidTokenTypeError(f"Expected a {expected_type.value} token")

            return payload

        except ExpiredSignatureError as ex:
            raise ExpiredTokenError() from ex
        except PyJwtError as ex:
            raise InvalidTokenError(str(ex)) from ex

    def issued_token(self, user: User) -> TokenPair:
        now = datetime.now(UTC)

        access_jti = uuid4()
        refresh_jti = uuid4()

        access_expires_at = now + self._config.access_token_lifetime
        refresh_expires_at = now + self._config.refresh_token_lifetime

        access_token = self._create_token(
            user_id=user.id,
            token_type=TokenType.ACCESS,
            issued_at=now,
            expires_at=access_expires_at,
            role=user.role,
            jti=access_jti,
        )

        refresh_token = self._create_token(
            user_id=user.id,
            token_type=TokenType.REFRESH,
            issued_at=now,
            expires_at=refresh_expires_at,
            role=user.role,
            jti=refresh_jti,
        )

        return TokenPair(access_token=access_token, refresh_token=refresh_token, refresh_jti=refresh_jti,
                         refresh_expires_at=refresh_expires_at)

    def decode_access_token(self, token: str) -> TokenPayload:
        return self._decode(token, TokenType.ACCESS)

    def decode_refresh_token(self, token: str) -> TokenPayload:
        return self._decode(token, TokenType.REFRESH)
