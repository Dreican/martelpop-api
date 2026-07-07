from pydantic import SecretStr, BaseModel


class OAuthConfig(BaseModel):
    google_client_id: str
    google_client_secret: SecretStr

    facebook_client_id: str
    facebook_client_secret: SecretStr

    frontend_url: str = "http://localhost:5173"
