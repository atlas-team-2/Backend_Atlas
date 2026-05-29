from datetime import timedelta
from functools import lru_cache

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
    secret: SecretStr = 'super_secure_secret_at_least_32_chars'
    algorithm: str = 'HS256'
    access_token_lifetime_seconds: int = int(timedelta(hours=1).total_seconds())
    refresh_token_lifetime_seconds: int = int(timedelta(days=1).total_seconds())


class RbacSettings(BaseSettings):
    admin_role: str = 'admin'
    public_role: str = 'public'
    admin_email: str = 'admin@atlas.ru'
    admin_password: str = 'admin'


class EmailSettings(BaseSettings):
    host: str = 'smtp.gmail.com'
    port: int = 587
    username: str = ''
    password: str = ''
    from_email: str = ''


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DbSettings = DbSettings()
    auth: AuthSettings = AuthSettings()
    rbac: RbacSettings = RbacSettings()
    email: EmailSettings = EmailSettings()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        extra='ignore',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
