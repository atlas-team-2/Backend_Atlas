from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str = "Atlas Naroda API"
    version: str = "1.0.0"
    description: str = "API для проекта Атлас народа"


class DbSettings(BaseSettings):
    schema: str = "postgresql+asyncpg"
    host: str = "localhost"
    user: str = "postgres"
    password: str = "postgres"
    port: int = 5432
    name: str = "atlas_db"


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DbSettings = DbSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
