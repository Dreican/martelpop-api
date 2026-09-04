from pydantic import BaseModel


class LogConfig(BaseModel):
    seq_url: str = "http://localhost:5341"
    level: str = "INFO"
    dir: str = "/code/logs"
    file: str = "application.log"
    error_file: str = "error.log"
    format: str = (
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(filename)s:%(lineno)d | "
        "%(message)s"
    )
