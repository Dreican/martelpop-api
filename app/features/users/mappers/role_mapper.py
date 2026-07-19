from app.features.auth.models.role import Role
from app.features.users.dto.role_response import RoleResponse


class RoleMapper:

    @staticmethod
    def to_response(role: Role) -> RoleResponse:
        return RoleResponse(
            code=role.code,
            name=role.name,
        )
