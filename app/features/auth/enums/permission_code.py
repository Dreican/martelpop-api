from enum import StrEnum


class PermissionCode(StrEnum):
    USER_READ = "user.read"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"
    USER_IMPERSONATE = "user.impersonate"

    ROLE_READ = "role.read"
    ROLE_UPDATE = "role.update"

    PERMISSION_READ = "permission.read"

    ROLE_PERMISSIONS_MANAGE = "role.permissions.manage"

    EVENT_CREATE = "event.create"
    EVENT_READ = "event.read"
    EVENT_UPDATE = "event.update"
    EVENT_DELETE = "event.delete"
    EVENT_PUBLISH = "event.publish"

    REGISTRATION_CREATE = "registration.create"
    REGISTRATION_CANCEL = "registration.cancel"
    REGISTRATION_MANAGE = "registration.manage"

    WAITLIST_MANAGE = "waitlist.manage"
