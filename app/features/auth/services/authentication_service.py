import logging
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services.slug_service import SlugService
from app.features.auth.dto.authentication_tokens import AuthenticationTokens
from app.features.auth.dto.login_request import LoginRequest
from app.features.auth.dto.register_request import RegisterRequest
from app.features.auth.dto.session_info import SessionInfo
from app.features.auth.dto.token_response import TokenResponse
from app.features.auth.enums.auth_provider import AuthProvider
from app.features.auth.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    DefaultRoleNotFoundError,
    RefreshTokenReuseDetected
)
from app.features.auth.models.authentication_identity import AuthenticationIdentity
from app.features.auth.models.refresh_token import RefreshToken
from app.features.auth.repositories.authentication_identity_repository import AuthenticationIdentityRepository
from app.features.auth.repositories.refresh_token_repository import RefreshTokenRepository
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.auth.services.jwt_service import JwtService
from app.features.auth.services.password_service import PasswordService
from app.features.users.enums.user_status import UserStatus
from app.features.users.models.user import User
from app.features.users.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class AuthenticationService:

    def __init__(
            self,
            session: AsyncSession,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            authentication_identity_repository: AuthenticationIdentityRepository,
            password_service: PasswordService,
            jwt_service: JwtService,
            refresh_token_repository: RefreshTokenRepository,
    ) -> None:
        self._session = session
        self._users = user_repository
        self._roles = role_repository
        self._identities = authentication_identity_repository
        self._password = password_service
        self._jwt = jwt_service
        self._refresh_tokens = refresh_token_repository

    async def register(self, request: RegisterRequest, session: SessionInfo) -> TokenResponse:
        try:
            await self._is_email_available(request.email)

            password_hash = await self._password.hash_password(request.password)
            user = await self._create_user(request)
            identity = self._create_local_identity(user=user, password_hash=password_hash)

            await self._users.add(user)
            await self._identities.add(identity)
            tokens = await self._issue_tokens(user, session)
            await self._refresh_tokens.add(tokens.refresh_token)

            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

        logger.info("User registered", extra={"user_id": user.id, "email": request.email})

        return tokens.response

    async def login(self, request: LoginRequest, session: SessionInfo) -> TokenResponse:
        identity = await self._identities.get_by_user_email(request.email)

        if identity is None:
            logger.warning("User doesn't exist", extra={"email": request.email})
            raise InvalidCredentialsError()

        if identity.password_hash is None:
            logger.error("User has no password", extra={"user_id": identity.user.id, "email": request.email})
            raise InvalidCredentialsError()

        if not identity.user.is_active:
            logger.warning("User is inactive", extra={"user_id": identity.user.id, "email": request.email})
            raise InvalidCredentialsError()

        if not self._password.verify_password(request.password, identity.password_hash):
            logger.warning("Invalid credentials", extra={"email": request.email})
            raise InvalidCredentialsError()

        async with self._session.begin():
            identity.last_login_at = datetime.now(UTC)
            tokens = await self._issue_tokens(identity.user, session)
            await self._refresh_tokens.add(tokens.refresh_token)

        logger.info("User logged in", extra={"user_id": identity.user.id, "email": identity.user.email})

        return tokens.response

    async def refresh(self, refresh_token: str, session: SessionInfo) -> TokenResponse:
        payload = self._jwt.decode_refresh_token(refresh_token)
        stored = await self._refresh_tokens.get_by_jti(payload.jti)

        if stored is None:
            logger.warning("Refresh token not found", extra={"payload_sub": payload.sub, "payload_jti": payload.jti})
            raise InvalidCredentialsError()

        if stored.is_revoked:
            logger.warning("Refresh token is revoked", extra={"payload_sub": payload.sub, "payload_jti": payload.jti})
            async with self._session.begin():
                await self._refresh_tokens.revoke_all_for_user(stored.user_id)

            raise RefreshTokenReuseDetected()

        if stored.is_expired:
            logger.warning("Refresh token is expired", extra={"payload_sub": payload.sub, "payload_jti": payload.jti})
            raise InvalidCredentialsError()

        if not self._password.verify_password(refresh_token, stored.token_hash):
            logger.warning("Invalid refresh token", extra={"payload_sub": payload.sub, "payload_jti": payload.jti})
            raise InvalidCredentialsError()

        user = stored.user

        if not user.is_active:
            logger.warning("User is inactive", extra={"user_id": user.id, "email": stored.user.email})
            raise InvalidCredentialsError()

        async with self._session.begin():
            stored.mark_used()
            tokens = await self._issue_tokens(user, session)
            await self._refresh_tokens.replace(current=stored, replacement=tokens.refresh_token)

        logger.info("Token refreshed", extra={"user_id": user.id, "email": stored.user.email})

        return tokens.response

    async def logout(self, refresh_token: str) -> None:
        payload = self._jwt.decode_refresh_token(refresh_token)

        revoked = await self._refresh_tokens.revoke(user_id=payload.sub, refresh_jti=payload.jti)
        await self._session.commit()

        if not revoked:
            logger.warning(
                "Attempted logout with unknown refresh token",
                extra={"user_id": payload.sub, "jti": payload.jti},
            )

    async def logout_all(self, user_id: UUID) -> None:
        async with self._session.begin():
            count = await self._refresh_tokens.revoke_all_for_user(user_id=user_id)

        logger.info(
            "%s sessions revoked",
            count,
            extra={"user_id": user_id},
        )

    async def _is_email_available(self, email: str) -> None:
        existing = await self._users.get_by_email(email)
        if existing is not None:
            logger.error("Email already exists", extra={"email": email})
            raise EmailAlreadyExistsError()

    async def _create_user(self, request: RegisterRequest) -> User:
        default_role = await self._roles.get_default_role()

        if default_role is None:
            logger.error("Default role not found")
            raise DefaultRoleNotFoundError()

        # inject the SlugService ?
        slug = await SlugService.create_unique(request.firstname, request.lastname, exists=self._users.exists_by_slug)

        logger.info("User created", extra={"email": request.email, "role": default_role.name})

        return User(
            email=request.email,
            firstname=request.firstname,
            lastname=request.lastname,
            slug=slug,
            status=UserStatus.ACTIVE,
            role=default_role
        )

    async def _issue_tokens(self, user: User, session: SessionInfo) -> AuthenticationTokens:
        tokens = self._jwt.issue_tokens(user=user)
        token_hash = await self._password.hash_password(tokens.refresh_token)

        refresh = RefreshToken(
            user=user,
            jti=tokens.refresh_jti,
            token_hash=token_hash,
            expires_at=tokens.refresh_expires_at,
            user_agent=session.user_agent,
            ip_address=session.ip_address,
            device_name=session.device_name,
        )

        logger.info("Tokens issued", extra={"user_id": user.id, "email": user.email})

        return AuthenticationTokens(
            response=tokens.to_response(),
            refresh_token=refresh
        )

    @staticmethod
    def _create_local_identity(user: User, password_hash: str) -> AuthenticationIdentity:
        return AuthenticationIdentity(
            user=user,
            provider=AuthProvider.LOCAL,
            password_hash=password_hash
        )
