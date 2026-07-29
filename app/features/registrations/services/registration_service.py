from app.core.services.base_service import BaseService


class RegistrationService(BaseService):
    def __init__(self, session):
        super().__init__(session)