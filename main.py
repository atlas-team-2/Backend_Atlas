from pathlib import Path

import yaml
from fastapi import FastAPI

app = FastAPI(
    title='Atlas Naroda API',
    version='1.0.0',
    description='API для проекта Атлас народа',
)

SPEC_PATH = Path(__file__).parent / 'openapi_atlas.yaml'


@app.get('/')
def read_root():
    return {'message': 'Atlas Naroda API is running'}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    with open(SPEC_PATH, 'r', encoding='utf-8') as file:
        app.openapi_schema = yaml.safe_load(file)

    return app.openapi_schema


app.openapi = custom_openapi
