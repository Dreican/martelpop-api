from fastapi import APIRouter, status, Cookie
from fastapi import Response

from app.features.auth.dependencies.current_principal import AuthenticatedPrincipalDep
from app.features.auth.dependencies.services import AuthServiceDep
from app.features.auth.dependencies.session import SessionInfoDep
from app.features.auth.dto.requests.login_request import LoginRequest
from app.features.auth.dto.requests.register_request import RegisterRequest
from app.features.auth.dto.responses.token_response import TokenResponse
from app.features.auth.exceptions.helper import unauthorized
from app.features.auth.security.refresh_cookie import set_refresh_token, clear_refresh_token_cookie

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Email already exists"},
    }
)
async def register(
        request: RegisterRequest,
        response: Response,
        auth: AuthServiceDep,
        session: SessionInfoDep
) -> TokenResponse:
    tokens = await auth.register(request, session)
    set_refresh_token(response, tokens.raw_refresh_token)

    return tokens.response


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    description="Authenticates a user and returns an access token.",
    responses={
        401: {"description": "Invalid credentials"},
    }
)
async def login(
        request: LoginRequest,
        response: Response,
        auth: AuthServiceDep,
        session: SessionInfoDep
) -> TokenResponse:
    tokens = await auth.login(request, session)
    set_refresh_token(response, tokens.raw_refresh_token)

    return tokens.response


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def refresh(
        response: Response,
        auth: AuthServiceDep,
        session: SessionInfoDep,
        refresh_token: str | None = Cookie(
            default=None,
            alias="refresh_token"
        )
) -> TokenResponse:
    if refresh_token is None:
        unauthorized("Missing refresh token")

    token = await auth.refresh(refresh_token, session)
    set_refresh_token(response, token.raw_refresh_token)

    return token.response


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(
        response: Response,
        auth: AuthServiceDep,
        refresh_token: str | None = Cookie(
            default=None,
            alias="refresh_token",
        )
) -> Response:
    if refresh_token is not None:
        await auth.logout(refresh_token)

    clear_refresh_token_cookie(response)

    return response


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout_all(
        principal: AuthenticatedPrincipalDep,
        response: Response,
        auth: AuthServiceDep
) -> Response:
    await auth.logout_all(principal.user.id)

    clear_refresh_token_cookie(response)
    return response
