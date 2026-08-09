from app.core.factories.response_factory import ResponseFactory
from app.features.auth.dto.responses.persmission_summary_response import PermissionSummaryResponse
from app.features.auth.dto.responses.role_response import RoleResponse
from app.features.auth.dto.responses.role_summary_response import RoleSummaryResponse
from app.features.auth.factories.permission_summary_response_factory import PermissionSummaryResponseFactory
from app.features.auth.models.role import Role
from app.features.storage.services.sotrage_service import StorageService


class RoleResponseFactory(ResponseFactory[Role, RoleResponse]):
    def __init__(self, storage: StorageService, permission: PermissionSummaryResponseFactory):
        super().__init__(storage)
        self._permission = permission

    def create(self, entity: Role) -> RoleResponse:
        response = RoleResponse.model_validate(entity)

        response.permissions = self._permission.create_many(entity.permissions)

        return response