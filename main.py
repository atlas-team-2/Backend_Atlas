from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db import create_db_and_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan,
)


@app.get('/')
async def read_root():
    return {'message': 'Atlas Naroda API is running'}


@app.get('/items/{item_id}')
def read_item(item_id: int):
    return {'item_id': item_id}
