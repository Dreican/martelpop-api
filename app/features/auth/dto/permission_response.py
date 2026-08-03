from app.features.auth.dto.persmission_summary_response import PermissionSummaryResponse
from app.features.auth.dto.role_summary_response import RoleSummaryResponse


class PermissionResponse(PermissionSummaryResponse):
    description: str
    roles: list[RoleSummaryResponse]