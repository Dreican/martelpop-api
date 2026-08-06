from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.core.dependencies.response_factories import RegistrationResponseFactoryDep
from app.features.events.dependencies.repositories import EventRepositoryDep
from app.features.registrations.dependencies.policies import RegistrationPolicyDep
from app.features.registrations.dependencies.repositories import RegistrationRepositoryDep
from app.features.registrations.services.registration_service import RegistrationService
from app.features.settings.dependencies.settings import ApplicationSettingsDep


def get_registration_service(
        session: SessionDep,
        registration_repository: RegistrationRepositoryDep,
        event_repository: EventRepositoryDep,
        registration_policy: RegistrationPolicyDep,
        response_factory: RegistrationResponseFactoryDep,
        application_settings: ApplicationSettingsDep
) -> RegistrationService:
    return RegistrationService(
        session=session,
        registration_repository=registration_repository,
        event_repository=event_repository,
        registration_policy=registration_policy,
        registration_response=response_factory,
        application_settings=application_settings
    )


RegistrationServiceDep = Annotated[RegistrationService, Depends(get_registration_service)]
