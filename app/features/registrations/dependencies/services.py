from typing import Annotated

from fastapi import Depends

from app.core.dependencies.database import SessionDep
from app.core.dependencies.response_factories import (
    RegistrationResponseFactoryDep,
    RegistrationSummaryResponseFactoryDep
)
from app.features.events.dependencies.repositories import EventRepositoryDep
from app.features.registrations.dependencies.policies import RegistrationPolicyDep
from app.features.registrations.dependencies.repositories import RegistrationRepositoryDep
from app.features.registrations.services.registration_service import RegistrationService
from app.features.settings.dependencies.settings import ApplicationSettingsDep
from app.features.users.dependencies.repositories import UserRepositoryDep


def get_registration_service(
        session: SessionDep,
        registration_repository: RegistrationRepositoryDep,
        event_repository: EventRepositoryDep,
        user_repository: UserRepositoryDep,
        registration_policy: RegistrationPolicyDep,
        response_factory: RegistrationResponseFactoryDep,
        response_summary_factory: RegistrationSummaryResponseFactoryDep,
        application_settings: ApplicationSettingsDep
) -> RegistrationService:
    return RegistrationService(
        session=session,
        registration_repository=registration_repository,
        event_repository=event_repository,
        user_repository=user_repository,
        registration_policy=registration_policy,
        registration_response=response_factory,
        registration_summary_response=response_summary_factory,
        application_settings=application_settings
    )


RegistrationServiceDep = Annotated[RegistrationService, Depends(get_registration_service)]
