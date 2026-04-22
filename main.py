from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
)

@app.get('/')
async def read_root():
    return {'message': 'Atlas Naroda API is running'}
