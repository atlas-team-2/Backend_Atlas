from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Atlas Naroda API'
    app_version: str = '1.0.0'
    app_description: str = 'API для проекта Атлас народа'

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

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.db_user}:{self.db_password}'
            f'@{self.db_host}:{self.db_port}/{self.db_name}'
        )


settings = Settings()
