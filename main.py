from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import settings
from app.db.engine import create_db_and_tables
from app.routers import auth, user


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    lifespan=lifespan,
)


@app.get('/')
async def read_root():
    return {'message': 'Atlas Naroda API is running'}


app.include_router(auth.router, prefix='/api/v1')
app.include_router(user.router, prefix='/api/v1')
