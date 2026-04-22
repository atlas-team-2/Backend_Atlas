from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class AppConfig(BaseModel):
    name: str = 'Atlas Naroda API'
    version: str = '1.0.0'
    description: str = 'API для проекта Атлас народа'


class DbConfig(BaseModel):
    drivername: str = 'postgresql+asyncpg'
    host: str = 'localhost'
    user: str = 'postgres'
    password: str = "postgres"
    port: int = 5432
    name: str = 'atlas_db'
    schema: str = "public"

    @property
    def url(self) -> str:
        return str(
            URL.create(
                drivername=self.drivername,
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.name,
            )
        )


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
