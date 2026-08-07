from typing import Annotated

from fastapi import HTTPException, status, Depends

from app.features.auth.dependencies.current_principal import CurrentPrincipalDep
from app.features.settings.dependencies.settings import ApplicationSettingsDep


async def require_not_in_maintenance(principal: CurrentPrincipalDep, settings: ApplicationSettingsDep) -> None:
    general = await settings.general()

    if not general.maintenance_mode:
        return

    if principal.is_admin:
        return

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="The application is currently under maintenance.",
    )


MaintenanceDep = Annotated[
    None,
    Depends(require_not_in_maintenance),
]
