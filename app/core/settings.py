from datetime import timedelta

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str = 'Atlas Naroda API'
    version: str = '0.1.0'
    description: str = 'Atlas Naroda backend API'


class DbSettings(BaseSettings):
    schema: str = 'postgresql+asyncpg'
    host: str = 'localhost'
    port: int = 5432
    name: str = 'atlas_db'
    user: str = 'postgres'
    password: str = 'postgres'


class AuthSettings(BaseSettings):
    secret: SecretStr
    algorithm: str = 'HS256'
    access_token_lifetime_seconds: int = 900
    refresh_token_lifetime_seconds: int = 604800

    @property
    def access_token_lifetime(self) -> timedelta:
        return timedelta(seconds=self.access_token_lifetime_seconds)

    @property
    def refresh_token_lifetime(self) -> timedelta:
        return timedelta(seconds=self.refresh_token_lifetime_seconds)


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DbSettings
    auth: AuthSettings

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        extra='ignore',
    )


settings = Settings()
