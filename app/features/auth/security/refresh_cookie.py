from typing import Final

from fastapi import Response

from app.core.config.configuration import get_config
from app.features.auth.models.refresh_token import RefreshToken

REFRESH_COOKIE_NAME: Final = "refresh_token"
config = get_config()


def set_refresh_token(response: Response, refresh_token: RefreshToken) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token.token_hash,
        httponly=True,
        secure=config.cookie.secure,
        samesite=config.cookie.samesite,
        path=f"{config.app.api_prefix}/auth",
    )


def clear_refresh_token_cookie(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        httponly=True,
        secure=config.cookie.secure,
        samesite=config.cookie.samesite,
        path=f"{config.app.api_prefix}/auth",
    )
