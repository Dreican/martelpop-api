from typing import Annotated

from fastapi import Depends

from app.features.registrations.policies.registration_policy import RegistrationPolicy


def get_registration_policy() -> RegistrationPolicy:
    return RegistrationPolicy()


RegistrationPolicyDep = Annotated[RegistrationPolicy, Depends(get_registration_policy)]
