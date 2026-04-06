from pathlib import Path
from fastapi import FastAPI

app = FastAPI(
    title='Atlas Naroda API',
    version='1.0.0',
    description='API для проекта Атлас народа',
)


@app.get('/')
def read_root():
    return {'message': 'Atlas Naroda API is running'}

