from pydantic import BaseModel


class LogConfig(BaseModel):
    level: str = "INFO"
    dir: str = "/code/logs"
    file: str = "application.log"
