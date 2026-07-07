from pydantic import computed_field, BaseModel


class DatabaseConfig(BaseModel):
    host: str = "db"
    port: int = 5432
    name: str = "martelpop"
    user: str = "martelpop"
    password: str = "martelpop"

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
