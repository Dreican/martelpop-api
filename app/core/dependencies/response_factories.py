from typing import Annotated

from fastapi import Depends

from app.features.auth.factories.permission_summary_response_factory import PermissionSummaryResponseFactory
from app.features.auth.factories.role_response_factory import RoleResponseFactory
from app.features.auth.factories.role_summary_response_factory import RoleSummaryResponseFactory
from app.features.events.factories.activity_type_admin_response_factory import ActivityTypeAdminResponseFactory
from app.features.events.factories.activity_type_response_factory import ActivityTypeResponseFactory
from app.features.events.factories.activity_type_summary_response_factory import ActivityTypeSummaryResponseFactory
from app.features.events.factories.event_response_factory import EventResponseFactory
from app.features.events.factories.event_summary_response_factory import EventSummaryResponseFactory
from app.features.events.factories.participant_response_factory import ParticipantResponseFactory
from app.features.registrations.factories.registration_response_factory import RegistrationResponseFactory
from app.features.registrations.factories.registration_summary_response_factory import \
    RegistrationSummaryResponseFactory
from app.features.storage.factories.stored_file_response_factory import StoredFileResponseFactory
from app.features.users.factories.user_admin_response_factory import UserAdminResponseFactory
from app.features.users.factories.user_response_factory import UserResponseFactory
from app.features.users.factories.user_summary_response_factory import UserSummaryResponseFactory


def get_stored_file_response_factory() -> StoredFileResponseFactory:
    return StoredFileResponseFactory()


StoredFileResponseFactoryDep = Annotated[
    StoredFileResponseFactory, Depends(get_stored_file_response_factory)]


def get_permission_summary_response_factory() -> PermissionSummaryResponseFactory:
    return PermissionSummaryResponseFactory()


PermissionSummaryResponseFactoryDep = Annotated[
    PermissionSummaryResponseFactory, Depends(get_permission_summary_response_factory)]


def get_role_response_factory(permission: PermissionSummaryResponseFactoryDep) -> RoleResponseFactory:
    return RoleResponseFactory(permission=permission)


def get_role_summary_response_factory() -> RoleSummaryResponseFactory:
    return RoleSummaryResponseFactory()


RoleResponseFactoryDep = Annotated[RoleResponseFactory, Depends(get_role_response_factory)]
RoleSummaryResponseFactoryDep = Annotated[RoleSummaryResponseFactory, Depends(get_role_summary_response_factory)]


def get_user_response_factory(role: RoleSummaryResponseFactoryDep) -> UserResponseFactory:
    return UserResponseFactory(role=role)


def get_user_summary_response_factory() -> UserSummaryResponseFactory:
    return UserSummaryResponseFactory()


def get_user_admin_response_factory(role: RoleSummaryResponseFactoryDep) -> UserAdminResponseFactory:
    return UserAdminResponseFactory(role=role)


UserResponseFactoryDep = Annotated[UserResponseFactory, Depends(get_user_response_factory)]
UserSummaryResponseFactoryDep = Annotated[UserSummaryResponseFactory, Depends(get_user_summary_response_factory)]
UserAdminResponseFactoryDep = Annotated[UserAdminResponseFactory, Depends(get_user_admin_response_factory)]


def get_activity_type_summary_response_factory() -> ActivityTypeSummaryResponseFactory:
    return ActivityTypeSummaryResponseFactory()


def get_activity_type_response_factory() -> ActivityTypeResponseFactory:
    return ActivityTypeResponseFactory()


def get_activity_type_admin_response_factory(user: UserSummaryResponseFactoryDep) -> ActivityTypeAdminResponseFactory:
    return ActivityTypeAdminResponseFactory(user=user)


ActivityTypeSummaryResponseFactoryDep = Annotated[
    ActivityTypeSummaryResponseFactory,
    Depends(get_activity_type_summary_response_factory)
]

ActivityTypeResponseFactoryDep = Annotated[ActivityTypeResponseFactory, Depends(get_activity_type_response_factory)]

ActivityTypeAdminResponseFactoryDep = Annotated[
    ActivityTypeAdminResponseFactory,
    Depends(get_activity_type_admin_response_factory)
]


def get_event_response_factory(
        activity_type_factory: ActivityTypeResponseFactoryDep,
        user_factory: UserResponseFactoryDep
) -> EventResponseFactory:
    return EventResponseFactory(
        activity_type_factory=activity_type_factory,
        user_factory=user_factory
    )


def get_event_summary_response_factory(
        activity_type_summary_factory: ActivityTypeSummaryResponseFactoryDep,
) -> EventSummaryResponseFactory:
    return EventSummaryResponseFactory(
        activity_type_summary_factory=activity_type_summary_factory,
    )


EventResponseFactoryDep = Annotated[EventResponseFactory, Depends(get_event_response_factory)]
EventSummaryResponseFactoryDep = Annotated[EventSummaryResponseFactory, Depends(get_event_summary_response_factory)]


def get_registration_response_factory(
        event_factory: EventSummaryResponseFactoryDep,
        user_factory: UserSummaryResponseFactoryDep
) -> RegistrationResponseFactory:
    return RegistrationResponseFactory(event_factory=event_factory, user_factory=user_factory)


def get_registration_summary_response_factory() -> RegistrationSummaryResponseFactory:
    return RegistrationSummaryResponseFactory()


def get_participant_response_factory(user_factory: UserSummaryResponseFactoryDep) -> ParticipantResponseFactory:
    return ParticipantResponseFactory(user_factory=user_factory)


RegistrationResponseFactoryDep = Annotated[RegistrationResponseFactory, Depends(get_registration_response_factory)]
RegistrationSummaryResponseFactoryDep = Annotated[
    RegistrationSummaryResponseFactory, Depends(get_registration_summary_response_factory)]
ParticipantResponseFactoryDep = Annotated[ParticipantResponseFactory, Depends(get_participant_response_factory)]
