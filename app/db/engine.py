from collections.abc import AsyncGenerator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def form_db_url() -> str:
    return URL.create(
        drivername=settings.db.schema,
        username=settings.db.user,
        password=settings.db.password,
        host=settings.db.host,
        port=settings.db.port,
        database=settings.db.name,
    ).render_as_string(hide_password=False)


engine = create_async_engine(
    form_db_url(),
    echo=False,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
