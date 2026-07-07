from pydantic import BaseModel


class SMTPConfig(BaseModel):
    host: str
    port: int = 587
    username: str
    password: str
    from_email: str = "noreply@martelpop.dev"
    use_tls: bool = True
