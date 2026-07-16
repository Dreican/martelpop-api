from datetime import datetime, UTC

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.dto.authentication_tokens import AuthenticationTokens
from app.features.auth.dto.login_request import LoginRequest
from app.features.auth.dto.register_request import RegisterRequest
from app.features.auth.dto.session_info import SessionInfo
from app.features.auth.dto.token_response import TokenResponse
from app.features.auth.enums.auth_provider import AuthProvider
from app.features.auth.exceptions import EmailAlreadyExistsError, InvalidCredentialsError, \
    DefaultRoleNotFoundError, RefreshTokenReuseDetected
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
        await self._is_email_available(request.email)

        password_hash = await self._password.hash_password(request.password)
        user = await self._create_user(request)
        identity = self._create_local_identity(user=user, password_hash=password_hash)

        async with self._session.begin():
            await self._users.add(user)
            await self._identities.add(identity)
            tokens = await self._issue_tokens(user, session)
            await self._refresh_tokens.add(tokens.refresh)

        return tokens.response

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
            tokens = await self._issue_tokens(identity.user, session)
            await self._refresh_tokens.add(tokens.refresh)

        return tokens.response

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
            tokens = await self._issue_tokens(user, session)
            await self._refresh_tokens.replace(current=stored, replacement=tokens.refresh)

        return tokens.response

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

    async def _issue_tokens(self, user: User, session: SessionInfo) -> AuthenticationTokens:
        issued_token = self._jwt.issued_token(user=user)
        token_hash = await self._password.hash_password(issued_token.refresh_token)

        refresh = RefreshToken(
            user=user,
            jti=issued_token.refresh_jti,
            token_hash=token_hash,
            expires_at=issued_token.refresh_expires_at,
            user_agent=session.user_agent,
            ip_address=session.ip_address,
            device_name=session.device_name,
        )

        return AuthenticationTokens(
            response=issued_token.to_response(),
            refresh=refresh
        )

    @staticmethod
    def _create_local_identity(user: User, password_hash: str) -> AuthenticationIdentity:
        return AuthenticationIdentity(
            user=user,
            provider=AuthProvider.LOCAL,
            password_hash=password_hash
        )
