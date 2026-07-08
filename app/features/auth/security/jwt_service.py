from datetime import datetime, timedelta, UTC
from uuid import UUID

import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError as PyJwtError

from app.core.config.jwt import JWTConfig
from app.features.auth.enums.token_type import TokenType
from app.features.auth.exceptions import (
    ExpiredTokenError,
    InvalidTokenError, InvalidTokenTypeError,
)

from app.features.auth.security.token_payload import TokenPayload
from app.features.users.enums.user_role import UserRole


class JwtService:

    def __init__(self, config: JWTConfig):
        self._config = config

    @property
    def _signing_key(self) -> str:
        return self._config.secret_key.get_secret_value()

    def _create_token(self, *, user_id: UUID, token_type: TokenType, expires_delta: timedelta,
                      role: UserRole | None = None) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "type": token_type.value,
            "iat": now,
            "exp": now + expires_delta,
            "iss": self._config.issuer,
            "aud": self._config.audience,
        }

        if role is not None:
            payload["role"] = role.value

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

    def create_access_token(self, user_id: UUID, role: UserRole) -> str:
        return self._create_token(
            user_id=user_id,
            token_type=TokenType.ACCESS,
            expires_delta=self._config.access_token_lifetime,
            role=role,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        return self._create_token(
            user_id=user_id,
            token_type=TokenType.REFRESH,
            expires_delta=self._config.refresh_token_lifetime,
        )

    def decode_access_token(self, token: str) -> TokenPayload:
        return self._decode(token, TokenType.ACCESS)

    def decode_refresh_token(self, token: str) -> TokenPayload:
        return self._decode(token, TokenType.REFRESH)