from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.role_code import RolesCode
from app.features.auth.models.role import Role


async def seed_roles(session: AsyncSession) -> None:
    roles = [
        Role(
            code=RolesCode.ADMIN,
            name="Administrator",
            description="Full access to the application",
            is_default=False
        ),
        Role(
            code=RolesCode.ORGANIZER,
            name="Organizer",
            description="Can manage event",
            is_default=False
        ),
        Role(
            code=RolesCode.VIP,
            name="VIP",
            description="VIP access",
            is_default=False
        ),
        Role(
            code=RolesCode.USER,
            name="User",
            description="Basic user access",
            is_default=True
        ),
    ]

    for role in roles:
        exists = await session.scalar(
            select(Role).where(Role.code == role.code)
        )

        if exists is None:
            session.add(role)