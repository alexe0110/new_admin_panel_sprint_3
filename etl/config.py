from pydantic import Field
from pydantic_settings import BaseSettings

from etl.index_schema import movies_schema


class PostgresSettings(BaseSettings):
    host: str = Field("127.0.0.1")
    port: str = Field("5432")
    dbname: str = Field(default="movies_database")
    user: str = Field(default="app")
    password: str = Field(default="123qwe")
    connect_timeout: int = 1

    class Config:
        env_prefix = "DB_"


class RedisSettings(BaseSettings):
    """Redis connection settings."""

    host: str = Field("127.0.0.1")
    port: int = Field(6379)

    class Config:
        env_prefix = "REDIS_"


class ElasticsearchConnection(BaseSettings):
    """Elasticsearch connection settings."""

    hosts: str = Field("http://localhost:9200", env="ES_HOST")


class ElasticsearchSettings(BaseSettings):
    """Elasticsearch index settings."""

    connection: ElasticsearchConnection = ElasticsearchConnection()
    index: str = "movies"
    index_schema: dict = movies_schema


class Settings(BaseSettings):
    """Project settings."""

    postgres: PostgresSettings = PostgresSettings()
    es: ElasticsearchSettings = ElasticsearchSettings()
    redis_settings: RedisSettings = RedisSettings()
    delay: int = 1
    page_size: int = 1000
    entities: set[str] = ("film_work", "person", "genre")
    debug: str = Field("INFO", env="DEBUG")
