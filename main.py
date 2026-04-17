from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import app_settings
from app.db import create_db_and_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title=app_settings.app_name,
    version=app_settings.app_version,
    description=app_settings.app_description,
    lifespan=lifespan,
)


@app.get('/')
async def read_root():
    return {'message': 'Atlas Naroda API is running'}
