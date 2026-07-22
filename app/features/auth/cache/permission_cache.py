from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.enums.role_code import RolesCode


class PermissionCache:
    def __init__(self):
        self._cache: dict[RolesCode, set[PermissionCode]] = {}

    def get(self, role: RolesCode) -> set[PermissionCode] | None:
        return self._cache.get(role)

    def add(self, role: RolesCode, permissions: set[PermissionCode]) -> None:
        self._cache[role] = permissions

    def invalidate(self, role: RolesCode) -> None:
        self._cache.pop(role, None)

    def clear(self) -> None:
        self._cache.clear()
