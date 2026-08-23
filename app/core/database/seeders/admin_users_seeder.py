from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.auth_provider import AuthProvider
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.models.authentication_identity import AuthenticationIdentity
from app.features.auth.models.role import Role
from app.features.auth.services.password_service import PasswordService
from app.features.users.enums.user_status import UserStatus
from app.features.users.models.user import User


SYSTEM_USER_EMAIL = "administrator@martelpop.internal"

async def seed_admin_users(session: AsyncSession, password_service: PasswordService) -> None:
    role = await session.scalar(
        select(Role).where(Role.code == RoleCode.ADMIN)
    )

    if role is None:
        raise RuntimeError("Administrator role must be seeded before the admin user")

    exist = await session.scalar(
        select(User).where(User.email == SYSTEM_USER_EMAIL)
    )

    if exist:
        return

    password_hash = await password_service.hash_password("Administrator")

    user = User(
        email=SYSTEM_USER_EMAIL,
        display_name="Administrator",
        firstname="System",
        lastname="Administrator",
        slug="administrator",
        status=UserStatus.ACTIVE,
        role=role,
        is_system=True
    )

    identity = AuthenticationIdentity(
        user=user,
        provider=AuthProvider.LOCAL,
        password_hash=password_hash,
    )

    session.add(user)
    session.add(identity)