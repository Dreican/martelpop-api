from fastapi import APIRouter, status
from fastapi import Response

from app.features.auth.dependencies.current_principal import AuthenticatedPrincipalDep
from app.features.auth.dependencies.services import AuthServiceDep
from app.features.auth.dependencies.session import SessionInfoDep
from app.features.auth.dto.requests.login_request import LoginRequest
from app.features.auth.dto.requests.logout_request import LogoutRequest
from app.features.auth.dto.requests.refresh_request import RefreshRequest
from app.features.auth.dto.requests.register_request import RegisterRequest
from app.features.auth.dto.responses.token_response import TokenResponse
from app.features.users.dto.user_response import UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(request: RegisterRequest, auth: AuthServiceDep, session: SessionInfoDep) -> TokenResponse:
    return await auth.register(request, session)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    description="Authenticates a user and returns an access token and refresh token.",
    responses={
        401: {"description": "Invalid credentials"},
        409: {"description": "Email already exists"},
    }
)
async def login(request: LoginRequest, auth: AuthServiceDep, session: SessionInfoDep) -> TokenResponse:
    return await auth.login(request, session)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def refresh(request: RefreshRequest, auth: AuthServiceDep, session: SessionInfoDep) -> TokenResponse:
    return await auth.refresh(request.refresh_token, session)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(request: LogoutRequest, auth: AuthServiceDep) -> Response:
    await auth.logout(request.refresh_token)
    return Response()


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout_all(principal: AuthenticatedPrincipalDep, auth: AuthServiceDep) -> Response:
    await auth.logout_all(principal.user.id)
    return Response()


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def me(principal: AuthenticatedPrincipalDep, auth: AuthServiceDep) -> UserResponse:
    return await auth.me(principal)
