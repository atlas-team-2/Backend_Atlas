from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = 'Atlas Naroda API'
    app_version: str = '1.0.0'
    app_description: str = 'API для проекта Атлас народа'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


class DatabaseSettings(BaseSettings):
    db_schema: str = 'postgresql+asyncpg'
    db_host: str = 'localhost'
    db_port: int = 5432
    db_name: str = 'atlas_db'
    db_user: str = 'postgres'
    db_password: str = 'postgres'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


app_settings = AppSettings()
db_settings = DatabaseSettings()
