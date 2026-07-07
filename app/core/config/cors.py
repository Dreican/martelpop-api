from pydantic import BaseModel


class CORSConfig(BaseModel):
    allowed_origins: list[str] = []
