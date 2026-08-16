from pydantic import BaseModel


class CORSConfig(BaseModel):
    backend_cors_origins: list[str] = []
