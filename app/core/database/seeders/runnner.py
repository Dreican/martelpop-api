from app.core.database.seeders.activity_type import seed_activity_types
from app.core.database.seeders.event_statuses_seeder import seed_event_status
from app.core.database.seeders.permission_seeder import seed_permissions
from app.core.database.seeders.role_permission_seeder import seed_role_permissions
from app.core.database.seeders.roles_seeder import seed_roles
from app.core.database.session import get_session_maker


async def seed_database() -> None:
    async with get_session_maker()() as session:
        async with session.begin():
            await seed_roles(session)
            await seed_permissions(session)
            await seed_role_permissions(session)
            await seed_activity_types(session)
            await seed_event_status(session)