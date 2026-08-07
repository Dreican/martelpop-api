from app.features.auth.security.authentication_token_extractor import AuthenticationTokenExtractor
from fastapi import WebSocket


class WebsocketTokenExtractor:

    @staticmethod
    def extract(websocket: WebSocket) -> str | None:

        authorization = websocket.headers.get("Authorization")

        if authorization is not None:
            scheme, _, token = authorization.partition(" ")

            if scheme.lower() == "bearer":
                return token or None

        return websocket.query_params.get("access_token")
