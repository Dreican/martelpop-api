from .app import AppSettings
from .cors import CORSSettings
from .database import DatabaseSettings
from .jwt import JWTSettings
from .logging import LogSettings
from .oauth import OAuthSettings
from .smtp import SMTPSettings
from .storage import StorageSettings


class Settings:
    def __init__(self):
        self.app = AppSettings()
        self.database = DatabaseSettings()
        self.jwt = JWTSettings()
        self.email = SMTPSettings()
        self.cors = CORSSettings()
        self.log = LogSettings()
        self.oauth = OAuthSettings()
        self.storage = StorageSettings()


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
