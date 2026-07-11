from datetime import datetime, UTC

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.dto.login_request import LoginRequest
from app.features.auth.dto.register_request import RegisterRequest
from app.features.auth.dto.token_response import TokenResponse
from app.features.auth.enums.auth_provider import AuthProvider
from app.features.auth.exceptions import EmailAlreadyExistsError, InvalidCredentialsError, UserNotFoundError, \
    DefaultRoleNotFoundError
from app.features.auth.models.authentication_identity import AuthenticationIdentity
from app.features.auth.repositories.authentication_identity_repository import AuthenticationIdentityRepository
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
    ) -> None:
        self._session = session
        self._users = user_repository
        self._roles = role_repository
        self._identities = authentication_identity_repository
        self._password = password_service
        self._jwt = jwt_service

    async def register(self, request: RegisterRequest) -> TokenResponse:
        await self._is_email_available(request.email)

        password_hash = await self._password.hash_password(request.password)
        user = await self._create_user(request)
        identity = self._create_local_identity(user=user, password_hash=password_hash)

        async with self._session.begin():
            await self._users.add(user)
            await self._identities.add(identity)

        return await self._create_token_response(user)

    async def login(self, request: LoginRequest) -> TokenResponse:
        identity = await self._identities.get_by_user_email(request.email)

        if identity is None:
            raise InvalidCredentialsError()

        if identity.password_hash is None:
            raise InvalidCredentialsError()

        if not self._password.verify_password(request.password, identity.password_hash):
            raise InvalidCredentialsError()

        identity.last_login_at = datetime.now(UTC)

        await self._session.commit()

        return await self._create_token_response(identity.user)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = self._jwt.decode_refresh_token(refresh_token)

        user = await self._users.get_by_id(payload.sub)

        if user is None:
            raise UserNotFoundError()

        if not user.is_active:
            raise InvalidCredentialsError()

        return await self._create_token_response(user)


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

    async def _create_token_response(self, user: User) -> TokenResponse:
        await self._session.refresh(user)
        access_token = self._jwt.create_access_token(user_id=user.id, role=user.role)

        refresh_token = self._jwt.create_refresh_token(user_id=user.id)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")

    @staticmethod
    def _create_local_identity(user: User, password_hash: str) -> AuthenticationIdentity:
        return AuthenticationIdentity(
            user=user,
            provider=AuthProvider.LOCAL,
            password_hash=password_hash
        )