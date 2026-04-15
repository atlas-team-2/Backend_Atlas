from fastapi import FastAPI

app = FastAPI(
    title='Atlas Naroda API',
    version='1.0.0',
    description='API для проекта Атлас народа',
)


@app.get('/')
def read_root():
    return {'message': 'Atlas Naroda API is running'}


@app.get('/items/{item_id}')
def read_item(item_id: int):
    return {'item_id': item_id}
