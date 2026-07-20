from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.models.permission import Permission


async def seed_permissions(session: AsyncSession) -> None:
    permissions_seed = (
        {
            "code": PermissionCode.USER_READ,
            "name": "Read user",
            "description": "Can read users",
        },
        {
            "code": PermissionCode.USER_UPDATE,
            "name": "Update user",
            "description": "Can edit users",
        },
        {
            "code": PermissionCode.USER_DELETE,
            "name": "Delete user",
            "description": "Can delete users",
        },
        {
            "code": PermissionCode.USER_MANAGE,
            "name": "Manage user",
            "description": "Can manage users",
        },
        {
            "code": PermissionCode.ROLE_CREATE,
            "name": "Create role",
            "description": "Can create roles",
        },
        {
            "code": PermissionCode.ROLE_READ,
            "name": "Read role",
            "description": "Can read roles",
        },
        {
            "code": PermissionCode.ROLE_UPDATE,
            "name": "Update role",
            "description": "Can update roles",
        },
        {
            "code": PermissionCode.EVENT_CREATE,
            "name": "Create event",
            "description": "Can create events",
        },
        {
            "code": PermissionCode.EVENT_UPDATE,
            "name": "Update event",
            "description": "Can edit events",
        },
        {
            "code": PermissionCode.EVENT_DELETE,
            "name": "Delete event",
            "description": "Can delete events",
        },
        {
            "code": PermissionCode.EVENT_MANAGE,
            "name": "Manage event",
            "description": "Can manage events",
        },
        {
            "code": PermissionCode.EVENT_READ,
            "name": "Read event",
            "description": "Can read events",
        },
    )

    for data in permissions_seed:
        exists = await session.scalar(
            select(Permission).where(Permission.code == data["code"])
        )

        if exists is None:
            session.add(Permission(**data))
        else:
            exists.name = data["name"]
            exists.description = data["description"]

