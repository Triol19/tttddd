from typing import Any, Dict, Optional

from lazy_load import lazy
from pydantic import BaseSettings, PostgresDsn, validator

__all__ = (
    'settings',
    'postgres_settings',
    'Settings',
    'PostgresSettings',
)


class Settings(BaseSettings):
    ENVIRONMENT: str = 'development'
    PROJECT_NAME: str = 'tttddd'


class PostgresSettings(BaseSettings):
    HOST: str
    PORT: int = 5432
    DB: str
    USER: str
    PASSWORD: str

    URI: Optional[PostgresDsn] = None

    # noinspection PyMethodParameters
    @validator('URI', pre=True)
    def connection(cls, v: Optional[str], values: Dict[str, str]) -> Any:
        if isinstance(v, str):
            return v

        path = '/' + path if (path := values.get('DB')) else None

        return PostgresDsn.build(
            scheme='postgresql',
            host=values.get('HOST'),
            port=str(values.get('PORT')),
            path=path,
            user=values.get('USER'),
            password=values.get('PASSWORD'),
        )

    class Config:
        env_prefix = 'POSTGRES_'


settings = lazy(Settings)
postgres_settings = lazy(PostgresSettings)
