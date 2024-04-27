from typing import Set
from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    """Postgres connection settings."""
    # todo сделаоь чтобы бралось из енв фалйа
    host: str = Field('127.0.0.1', env='DB_HOST')
    port: str = Field('5432', env='DB_PORT')
    dbname: str = Field(env='DB_NAME', default='movies_database')
    user: str = Field(env='DB_USER', default='app')
    password: str = Field(env='DB_PASSWORD', default='123qwe')
    connect_timeout: int = 1


class RedisSettings(BaseSettings):
    """Redis connection settings."""
    host: str = Field('127.0.0.1', env='REDIS_HOST')
    port: int = Field(6379, env='DEFAULT_REDIS_PORT')


class Settings(BaseSettings):
    """Project settings."""

    postgres: PostgresSettings = PostgresSettings()
    # es: ElasticsearchSettings = ElasticsearchSettings()
    redis_settings: RedisSettings = RedisSettings()
    delay: int = 1
    page_size: int = 1000
    entities: Set[str] = ('film_work', 'person', 'genre')
    debug: str = Field('INFO', env='DEBUG')

