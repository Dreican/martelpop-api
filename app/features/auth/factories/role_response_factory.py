from app.core.factories.response_factory import ResponseFactory
from app.features.auth.dto.responses.role_response import RoleResponse
from app.features.auth.factories.permission_summary_response_factory import PermissionSummaryResponseFactory
from app.features.auth.models.role import Role


class RoleResponseFactory(ResponseFactory[Role, RoleResponse]):
    def __init__(self, permission: PermissionSummaryResponseFactory):
        super().__init__()
        self._permission = permission

    def create(self, entity: Role) -> RoleResponse:
        response = RoleResponse.model_validate(entity)

        response.permissions = self._permission.create_many(entity.permissions)

        return response
