from pydantic import Field
from pydantic_settings import BaseSettings

from utils import es_schema


class PGSettings(BaseSettings):
    host: str = Field(default="127.0.0.1")
    port: str = Field(default="5432")
    dbname: str = Field(default="movies_database")
    user: str = Field(default="app")
    password: str = Field(default="123qwe")
    connect_timeout: int = 11

    class Config:
        env_prefix = "DB_"


class RedisSettings(BaseSettings):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=6379)

    class Config:
        env_prefix = "REDIS_"


class ElasticSettings(BaseSettings):
    es_addr: str = Field(default="http://127.0.0.1:9200")
    es_index: str = "movies"
    es_schema: dict = es_schema.movies_schema

    class Config:
        env_prefix = "ES_"


class Settings(BaseSettings):
    pg: PGSettings = PGSettings()
    es: ElasticSettings = ElasticSettings()
    redis_settings: RedisSettings = RedisSettings()
    tables: list = ["film_work", "person", "genre"]
