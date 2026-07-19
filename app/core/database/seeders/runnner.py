from app.core.database.seeders.roles_seeder import seed_roles
from app.core.database.session import get_session_maker


async def seed_database() -> None:
    async with get_session_maker()() as session:
        async with session.begin():
            await seed_roles(session)
