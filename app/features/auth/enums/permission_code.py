from enum import StrEnum


class PermissionCode(StrEnum):
    
    USER_READ = "user.read"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"
    USER_MANAGE = "user.manage"

    ROLE_CREATE = "role.create"
    ROLE_READ = "role.read"
    ROLE_UPDATE = "role.update"
    ROLE_DELETE = "role.delete"
    ROLE_MANAGE = "role.manage"

    PERMISSION_CREATE = "permission.create"
    PERMISSION_READ = "permission.read"
    PERMISSION_UPDATE = "permission.update"
    PERMISSION_DELETE = "permission.delete"
    PERMISSION_MANAGE = "permission.manage"

    EVENT_CREATE = "event.create"
    EVENT_READ = "event.read"
    EVENT_UPDATE = "event.update"
    EVENT_DELETE = "event.delete"
    EVENT_MANAGE = "event.manage"

    REGISTRATION_CREATE = "registration.create"
    REGISTRATION_READ = "registration.read"
    REGISTRATION_UPDATE = "registration.update"
    REGISTRATION_CANCEL = "registration.cancel"
    REGISTRATION_MANAGE = "registration.manage"

    WAITLIST_MANAGE = "waitlist.manage"
