from app.core.dependencies.database import SessionDep
from app.core.dependencies.slug import SlugServiceDep
from app.features.auth.repositories.authentication_identity_repository import AuthenticationIdentityRepository
from app.features.auth.repositories.role_repository import RoleRepository
from app.features.auth.services.password_service import PasswordService
from app.features.users.repositories.user_repository import UserRepository


class UserService:
    def __init__(
            self,
            session: SessionDep,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            authentication_identity_repository: AuthenticationIdentityRepository,
            password_service: PasswordService,
            slug_service: SlugServiceDep
    ):
        self._session = session
        self._users = user_repository
        self._roles = role_repository
        self._passwords = password_service
        self._authentication_identity = authentication_identity_repository
        self._slug = slug_service
