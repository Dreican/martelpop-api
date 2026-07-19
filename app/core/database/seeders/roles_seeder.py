from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.role_code import RolesCode
from app.features.auth.models.role import Role


async def seed_roles(session: AsyncSession) -> None:
    roles_seed = (
        {
            "code": RolesCode.ADMIN,
            "name": "Administrator",
            "description": "Full access to the application",
            "is_default": False
        },
        {
            "code": RolesCode.ORGANIZER,
            "name": "Organizer",
            "description": "Can manage event",
            "is_default": False
        },
        {
            "code": RolesCode.VIP,
            "name": "VIP",
            "description": "VIP access",
            "is_default": False
        },
        {
            "code": RolesCode.USER,
            "name": "User",
            "description": "Basic user access",
            "is_default": True
        },
    )

    for data in roles_seed:
        exists = await session.scalar(
            select(Role).where(Role.code == data["code"])
        )

        if exists is None:
            session.add(Role(**data))
        else:
            exists.name = data["name"]
            exists.description = data["description"]
            exists.is_default = data["is_default"]
