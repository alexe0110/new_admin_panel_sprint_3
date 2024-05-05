import pytest
from redis import Redis

from mover.components.extract import Extract
from mover.config import Settings
from mover.state import RedisStorage

test_settings = Settings()


@pytest.fixture()
def redis_connection():
    return Redis(**test_settings.redis_settings.model_dump())


@pytest.fixture()
def redis_storage(redis_connection) -> RedisStorage:
    return RedisStorage(redis_connection)


@pytest.fixture()
def pg_extractor(redis_connection):
    return Extract(pg_settings=test_settings.pg.model_dump(), redis_connection=redis_connection)
