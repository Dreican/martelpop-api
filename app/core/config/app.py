from pydantic import BaseModel


class AppConfig(BaseModel):
    name: str = "MartelPop API"
    version: str = "0.1.0"
    env: str = "DEV"
    host: str = "localhost"
    port: int = 8000
    api_prefix: str = "/api/v1"
    debug: bool = False
