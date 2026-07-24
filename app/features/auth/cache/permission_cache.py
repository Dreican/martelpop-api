from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RoleCode


class PermissionCache:
    def __init__(self):
        self._cache: dict[RoleCode, set[PermissionCode]] = {}

    def get(self, role: RoleCode) -> set[PermissionCode] | None:
        return self._cache.get(role)

    def add(self, role: RoleCode, permissions: set[PermissionCode]) -> None:
        self._cache[role] = permissions

    def invalidate(self, role: RoleCode) -> None:
        self._cache.pop(role, None)

    def clear(self) -> None:
        self._cache.clear()
