from pydantic_settings import BaseSettings

from utils import es_schema


class PGSettings(BaseSettings):
    host: str
    port: str
    dbname: str
    user: str
    password: str
    connect_timeout: int

    class Config:
        env_prefix = "DB_"


class RedisSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = "REDIS_"


class ElasticSettings(BaseSettings):
    addr: str
    index: str
    index_schema: dict = es_schema.movies_schema

    class Config:
        env_prefix = "ES_"


class Settings(BaseSettings):
    pg: PGSettings = PGSettings()
    es: ElasticSettings = ElasticSettings()
    redis_settings: RedisSettings = RedisSettings()
    tables: list = ["film_work", "person", "genre"]
