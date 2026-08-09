from uuid import UUID

from fastapi import APIRouter, status

from app.core.pagination.page import Page
from app.features.auth.dependencies.require_permissions import permission, authenticated_permission
from app.features.registrations.dto.requests.registration_create_request import RegistrationRequest
from app.features.auth.enums.permission_code import PermissionCode
from app.features.auth.security.principal import Principal, AuthenticatedPrincipal
from app.features.events.dependencies.services import EventServiceDep
from app.features.events.dto.responses.event_response import EventResponse
from app.features.registrations.dependencies.services import RegistrationServiceDep
from app.features.registrations.dto.requests.registration_search_request import RegistrationSearchRequest
from app.features.registrations.dto.requests.registration_update_request import RegistrationUpdateRequest
from app.features.registrations.dto.responses.registration_response import RegistrationResponse

router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"],
)


@router.get("/me", response_model=Page[RegistrationResponse], status_code=status.HTTP_200_OK)
async def search_events(
        request: RegistrationSearchRequest,
        registration_service: RegistrationServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission()
):
    return await registration_service.get_my_registrations(request, principal)


@router.delete("/{registration_id}", response_model=RegistrationResponse, status_code=status.HTTP_200_OK)
async def cancel(
        registration_id: UUID,
        registration_service: RegistrationServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.REGISTRATION_CANCEL)
):
    return await registration_service.cancel(registration_id, principal)


@router.get("/{registration_id}/undo", response_model=RegistrationResponse, status_code=status.HTTP_200_OK)
async def uncancel(
        registration_id: UUID,
        registration_service: RegistrationServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission(PermissionCode.REGISTRATION_CANCEL)
):
    return await registration_service.uncancel(registration_id, principal)


@router.patch("/{registration_id}", response_model=RegistrationResponse, status_code=status.HTTP_200_OK)
async def update(
        registration_id: UUID,
        request: RegistrationUpdateRequest,
        registration_service: RegistrationServiceDep,
        principal: AuthenticatedPrincipal = authenticated_permission()
):
    return await registration_service.update(registration_id, request, principal)


