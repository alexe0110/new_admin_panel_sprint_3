from typing import Set
from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    """Postgres connection settings."""
    # todo сделаоь чтобы бралось из енв фалйа
    host: str = Field('127.0.0.1')
    port: str = Field('5432')
    dbname: str = Field(default='movies_database')
    user: str = Field(default='app')
    password: str = Field(default='123qwe')
    connect_timeout: int = 1

    class Config:
        env_prefix = 'DB_'


class RedisSettings(BaseSettings):
    """Redis connection settings."""
    host: str = Field('127.0.0.1')
    port: int = Field(6379)

    class Config:
        env_prefix = 'REDIS_'


class Settings(BaseSettings):
    """Project settings."""

    postgres: PostgresSettings = PostgresSettings()
    # es: ElasticsearchSettings = ElasticsearchSettings()
    redis_settings: RedisSettings = RedisSettings()
    delay: int = 1
    page_size: int = 1000
    entities: Set[str] = ('film_work', 'person', 'genre')
    debug: str = Field('INFO', env='DEBUG')

