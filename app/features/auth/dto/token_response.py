from pydantic import BaseModel


class TokenResponse(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str