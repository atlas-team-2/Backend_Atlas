from collections.abc import AsyncGenerator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app import models  # noqa: F401
from app.core.config import db_settings


def form_db_url() -> str:
    return URL.create(
        drivername=db_settings.db_schema,
        username=db_settings.db_user,
        password=db_settings.db_password,
        host=db_settings.db_host,
        port=db_settings.db_port,
        database=db_settings.db_name,
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


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
