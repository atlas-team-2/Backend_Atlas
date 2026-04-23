from pydantic_settings import BaseSettings

class DBConfig(BaseSettings):
    schema: str = 'postgresql+asyncpg'
    host: str = 'localhost'
    user: str = 'postgres'
    password: str = 'postgres'
    port: int = 5432
    name: str = 'atlas_db'
