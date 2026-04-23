from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    name: str = 'Atlas Naroda API'
    version: str = '1.0.0'
    description: str = 'API для проекта Атлас народа'


class Settings(BaseSettings):
    app: AppConfig = AppConfig()

    db_schema: str = 'postgresql+asyncpg'
    db_host: str = 'localhost'
    db_user: str = 'postgres'
    db_password: str = 'postgres'
    db_port: int = 5432
    db_name: str = 'atlas_db'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='__',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
