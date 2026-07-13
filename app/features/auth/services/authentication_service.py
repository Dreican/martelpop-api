from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.jwt import JWTConfig
from app.features.auth.dto.login_request import LoginRequest
from app.features.auth.dto.register_request import RegisterRequest
from app.features.auth.dto.session_info import SessionInfo
from app.features.auth.dto.token_response import TokenResponse
from app.features.auth.dto.ìssued_tokens import IssuedTokens
from app.features.auth.enums.auth_provider import AuthProvider
from app.features.auth.exceptions import EmailAlreadyExistsError, InvalidCredentialsError, \
    DefaultRoleNotFoundError, RefreshTokenReuseDetected
from app.features.auth.models.authentication_identity import AuthenticationIdentity
from app.features.auth.models.refresh_token import RefreshToken
from app.features.auth.repositories.authentication_identity_repository import AuthenticationIdentityRepository
from app.features.auth.repositories.refresh_token_repository import RefreshTokenRepository
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.users.enums.user_status import UserStatus
from app.features.users.models.user import User
from app.features.auth.services.password_service import PasswordService
from app.features.auth.services.jwt_service import JwtService
from app.features.users.repositories.user_repository import UserRepository


class AuthenticationService:

    def __init__(
            self,
            session: AsyncSession,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            authentication_identity_repository: AuthenticationIdentityRepository,
            password_service: PasswordService,
            jwt_service: JwtService,
            jwt_config: JWTConfig,
            refresh_token_repository: RefreshTokenRepository,
    ) -> None:
        self._jwt_config = jwt_config
        self._session = session
        self._users = user_repository
        self._roles = role_repository
        self._identities = authentication_identity_repository
        self._password = password_service
        self._jwt = jwt_service
        self._refresh_tokens = refresh_token_repository

    async def register(self, request: RegisterRequest, session: SessionInfo) -> TokenResponse:
        await self._is_email_available(request.email)

        password_hash = await self._password.hash_password(request.password)
        user = await self._create_user(request)
        identity = self._create_local_identity(user=user, password_hash=password_hash)
        async with self._session.begin():
            await self._users.add(user)
            await self._identities.add(identity)
            issued_tokens = await self._issue_tokens(user, session)
            await self._refresh_tokens.add(issued_tokens.refresh_token)

        return issued_tokens.response

    async def login(self, request: LoginRequest, session: SessionInfo) -> TokenResponse:
        identity = await self._identities.get_by_user_email(request.email)

        if identity is None:
            raise InvalidCredentialsError()

        if identity.password_hash is None:
            raise InvalidCredentialsError()

        if not identity.user.is_active:
            raise InvalidCredentialsError()

        if not self._password.verify_password(request.password, identity.password_hash):
            raise InvalidCredentialsError()

        async with self._session.begin():
            identity.last_login_at = datetime.now(UTC)
            issued_tokens = await self._issue_tokens(identity.user, session)
            await self._refresh_tokens.add(issued_tokens.refresh_token)

        return issued_tokens.response

    async def refresh(self, refresh_token: str, session: SessionInfo) -> TokenResponse:
        payload = self._jwt.decode_refresh_token(refresh_token)
        stored = await self._refresh_tokens.get_by_jti(payload.jti)

        if stored is None:
            raise InvalidCredentialsError()

        if stored.is_revoked:
            async with self._session.begin():
                await self._refresh_tokens.revoke_all_for_user(stored.user_id)

            raise RefreshTokenReuseDetected()

        if stored.is_expired:
            raise InvalidCredentialsError()

        if not self._password.verify_password(refresh_token, stored.token_hash):
            raise InvalidCredentialsError()

        user = stored.user

        if not user.is_active:
            raise InvalidCredentialsError()

        async with self._session.begin():
            stored.mark_used()
            issued_tokens = await self._issue_tokens(user, session)
            await self._refresh_tokens.replace(current=stored, replacement=issued_tokens.refresh_token)


        return issued_tokens.response


    async def _is_email_available(self, email: str) -> None:
        existing = await self._users.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyExistsError()


    async def _create_user(self, request: RegisterRequest) -> User:
        default_role = await self._roles.get_default_role()

        if default_role is None:
            raise DefaultRoleNotFoundError()

        return User(
            email=request.email,
            firstname=request.firstname,
            lastname=request.lastname,
            status=UserStatus.ACTIVE,
            role=default_role
        )

    async def _issue_tokens(self, user: User, session: SessionInfo) -> IssuedTokens:
        now = datetime.now(UTC)
        access_expires_at = (now + self._jwt_config.access_token_lifetime)
        refresh_expires_at = (now + self._jwt_config.refresh_token_lifetime)
        access_jti = uuid4()
        refresh_jti = uuid4()

        access_token = self._jwt.create_access_token(user_id=user.id, role=user.role, jti=access_jti, issued_at=now, expires_at=access_expires_at)
        refresh_token = self._jwt.create_refresh_token(user_id=user.id, jti=refresh_jti, issued_at=now, expires_at=refresh_expires_at)

        token_hash = await self._password.hash_password(refresh_token)

        refresh = RefreshToken(
            user=user,
            jti=refresh_jti,
            token_hash=token_hash,
            expires_at=refresh_expires_at,
            user_agent=session.user_agent,
            ip_address=session.ip_address,
            device_name=session.device_name,
        )

        return IssuedTokens(
            response=TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="Bearer"),
            refresh_token=refresh
        )

    @staticmethod
    def _create_local_identity(user: User, password_hash: str) -> AuthenticationIdentity:
        return AuthenticationIdentity(
            user=user,
            provider=AuthProvider.LOCAL,
            password_hash=password_hash
        )