from datetime import timedelta
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str = 'Atlas Naroda API'
    version: str = '1.0.0'
    description: str = 'API для проекта Атлас народа'


class AuthSettings(BaseSettings):
    secret: SecretStr = 'change_me_to_openssl_secret_at_least_32_chars'
    algorithm: str = 'HS256'
    access_token_lifetime: timedelta = timedelta(hours=1)
    refresh_token_lifetime: timedelta = timedelta(days=1)


class DbSettings(BaseSettings):
    schema: str = 'postgresql+asyncpg'
    host: str = 'localhost'
    user: str = 'postgres'
    password: str = 'postgres'
    port: int = 5432
    name: str = 'atlas_db'


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DbSettings = DbSettings()
    auth: AuthSettings = AuthSettings()

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
