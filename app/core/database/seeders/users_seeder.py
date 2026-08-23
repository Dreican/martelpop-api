from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.role_code import RoleCode
from app.features.auth.models.role import Role
from app.features.users.enums.user_status import UserStatus
from app.features.users.models.user import User

SYSTEM_USER_SLUG = "system"
SYSTEM_USER_EMAIL = "system@martelpop.internal"

async def seed_users(session: AsyncSession) -> User:
    role = await get_system_role(session)

    users_seed = (
        {
            "email": SYSTEM_USER_EMAIL,
            "display_name": "Administrator",
            "firstname": "Full access to the application",
            "lastname": "",
            "slug": "",
            "status": UserStatus.ACTIVE,
            "role": role,
        },
    )

    for data in users_seed:
        exists = await session.scalar(
            select(User).where(User.slug == data["slug"])
        )

        if exists is None:
            session.add(Role(**data))
        # else:
        #     exists.name = data["name"]
        #     exists.description = data["description"]
        #     exists.is_default = data["is_default"]
