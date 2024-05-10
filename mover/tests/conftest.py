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
    return Extract(
        pg_settings=test_settings.pg.model_dump(),
        redis_connection=redis_connection,
        next_handler=lambda where_clause_table, pkeys: print(where_clause_table, pkeys),
    )


@pytest.fixture(autouse=False)
def _clean_redis(redis_connection: Redis):
    for db_in in range(15):
        with redis_connection as con:
            con.select(db_in)
            con.flushall()
