from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    name: str = 'Atlas Naroda API'
    version: str = '1.0.0'
    description: str = 'API для проекта Атлас народа'


class DbConfig(BaseModel):
    drivername: str = 'postgresql+asyncpg'
    host: str = 'localhost'
    user: str = 'postgres'
    password: str = 'ТВОЙ_РЕАЛЬНЫЙ_ПАРОЛЬ'
    port: int = 5432
    name: str = 'atlas_db'


class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    db: DbConfig = DbConfig()

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
