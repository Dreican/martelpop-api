from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RolesCode
from app.features.auth.models.permission import Permission
from app.features.auth.models.role import Role
from app.features.auth.models.role_permission import RolePermission


async def seed_role_permissions(session: AsyncSession) -> None:
    ROLE_PERMISSIONS = {
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
            PermissionCode.REGISTRATION_MANAGE,
        },
        RolesCode.VIP: {
            PermissionCode.EVENT_READ,
        },
        RolesCode.USER: {
            PermissionCode.EVENT_READ,
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

    for role_code, permission_codes in ROLE_PERMISSIONS.items():
        role = roles[role_code]

        for permission_code in permission_codes:
            permission = permissions[permission_code]

            exists = any(
                rp.permission_id == permission.id
                for rp in role.role_permissions
            )

            if not exists:
                role.role_permissions.append(
                    RolePermission(
                        permission=permission,
                    )
                )