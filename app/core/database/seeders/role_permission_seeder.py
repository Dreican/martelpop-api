from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RolesCode
from app.features.auth.models.permission import Permission
from app.features.auth.models.role import Role
from app.features.auth.models.role_permission import RolePermission


async def seed_role_permissions(session: AsyncSession) -> None:
    role_permissions_seed = {
        RolesCode.ADMIN: {
            PermissionCode.EVENT_READ,
            PermissionCode.EVENT_CREATE,
            PermissionCode.EVENT_UPDATE,
            PermissionCode.EVENT_DELETE,
            PermissionCode.EVENT_PUBLISH,
            PermissionCode.REGISTRATION_MANAGE,
            PermissionCode.ROLE_UPDATE,
        },
        RolesCode.ORGANIZER: {
            PermissionCode.EVENT_READ,
            PermissionCode.EVENT_CREATE,
            PermissionCode.EVENT_UPDATE,
            PermissionCode.EVENT_DELETE,
            PermissionCode.EVENT_PUBLISH,
        },
        RolesCode.VIP: {
            PermissionCode.EVENT_READ,
            PermissionCode.REGISTRATION_CREATE,
            PermissionCode.REGISTRATION_CANCEL
        },
        RolesCode.USER: {
            PermissionCode.EVENT_READ,
            PermissionCode.REGISTRATION_CREATE,
            PermissionCode.REGISTRATION_CANCEL
        },
    }

    roles = {
        role.code: role
        for role in (
            await session.scalars(select(Role))
        ).all()
    }

    permissions = {
        permission.code: permission
        for permission in (
            await session.scalars(select(Permission))
        ).all()
    }

    existing = {
        (rp.role_id, rp.permission_id)
        for rp in (
            await session.scalars(select(RolePermission))
        ).all()
    }

    for role_code, permission_codes in role_permissions_seed.items():
        role = roles[role_code]

        for permission_code in permission_codes:
            permission = permissions[permission_code]

            if (role.id, permission.id) not in existing:
                session.add(RolePermission(role=role, permission=permission))

                existing.add((role.id, permission.id))
