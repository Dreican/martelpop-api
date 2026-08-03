from typing import Annotated

from fastapi.params import Depends

from app.core.dependencies.database import SessionDep
from app.features.registrations.repositories.registration_repository import RegistrationRepository


def get_registration_repository(session: SessionDep) -> RegistrationRepository:
    return RegistrationRepository(session=session)


RegistrationRepositoryDep = Annotated[RegistrationRepository, Depends(get_registration_repository)]
