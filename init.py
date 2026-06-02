import asyncio

from app.db.engine import async_session_maker
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.services.bootstrapper import Bootstrapper


async def bootstrap_app() -> None:
    async with async_session_maker() as session:
        bootstrapper = Bootstrapper(
            role_repository=RoleRepository(session),
            permission_repository=PermissionRepository(session),
            user_repository=UserRepository(session),
        )
        await bootstrapper.bootstrap()


if __name__ == '__main__':
    asyncio.run(bootstrap_app())
