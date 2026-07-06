from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError as PyJwtError

from app.features.auth.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
)

from app.features.auth.enums import TokenType
from app.features.auth.security.jwt_config import JwtConfig
from app.features.auth.security.token_payload import TokenPayload
from app.features.users.enums import UserRole


class JwtService:

    def __init__(self, config: JwtConfig):
        self._config = config

    @property
    def _secret(self) -> str:
        return self._config.secret_key.get_secret_value()

    @property
    def _algorithm(self) -> str:
        return self._config.algorithm

    def _create_token(self, user_id: UUID, token_type: TokenType, expires_delta: timedelta, role: UserRole | None = None) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "role": role.value if role else None,
            "iat": now,
            "exp": now + expires_delta
        }

        if role is not None:
            payload["role"] = role.value

        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def create_access_token(self, user_id: UUID, role: UserRole) -> str:
        return self._create_token(
            user_id=user_id,
            token_type=TokenType.ACCESS,
            expires_delta=timedelta(minutes=self._config.access_token_expiration_minutes),
            role=role,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        return self._create_token(
            user_id=user_id,
            token_type=TokenType.REFRESH,
            expires_delta=timedelta(days=self._config.refresh_token_expiration_days),
        )

    def decode(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return TokenPayload.model_validate(payload)

        except ExpiredSignatureError as exc:
            raise ExpiredTokenError() from exc

        except PyJwtError as exc:
            raise InvalidTokenError() from exc
