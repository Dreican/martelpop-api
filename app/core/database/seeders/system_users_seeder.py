from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SYSTEM_USER_ID
from app.features.auth.enums.role_code import RoleCode
from app.features.auth.models.role import Role
from app.features.users.enums.user_status import UserStatus
from app.features.users.models.user import User

SYSTEM_USER_SLUG = "system"
SYSTEM_USER_EMAIL = "system@martelpop.internal"

async def seed_system_users(session: AsyncSession) -> None:
    role = await session.scalar(
        select(Role).where(Role.code == RoleCode.SYSTEM)
    )

    if role is None:
        raise RuntimeError("System role must be seeded before the system user")

    exist = await session.scalar(
        select(User).where(User.slug == SYSTEM_USER_SLUG)
    )

    if exist:
        return

    session.add(
        User(
            id=SYSTEM_USER_ID,
            email="system@martelpop.local",
            display_name="System",
            firstname="System",
            lastname="MartelPop",
            slug="system",
            status=UserStatus.ACTIVE,
            role=role,
            is_system=True
        )
    )