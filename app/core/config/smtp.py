from pydantic import BaseModel, SecretStr


class SMTPConfig(BaseModel):
    host: str
    port: int = 587
    username: str
    password: SecretStr
    from_email: str = "noreply@martelpop.dev"
    use_tls: bool = True
