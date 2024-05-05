from pydantic_settings import BaseSettings
from pydantic import Field


class PGSettings(BaseSettings):
    host: str = Field(default="127.0.0.1")
    port: str = Field(default="5432")
    dbname: str = Field(default="movies_database")
    user: str = Field(default="app")
    password: str = Field(default="123qwe")
    connect_timeout: int = 1

    class Config:
        env_prefix = "DB_"


class Settings(BaseSettings):
    pg: PGSettings = PGSettings()
