import pytest
from redis import Redis

from mover.components import Enricher, Extract
from mover.config import Settings
from mover.state import RedisStorage

test_settings = Settings()


@pytest.fixture()
def redis_connection(redis_db: int=0):
    return Redis(**test_settings.redis_settings.model_dump(), db=redis_db)


@pytest.fixture()
def redis_storage(redis_connection) -> RedisStorage:
    return RedisStorage(redis_connection)


@pytest.fixture()
def pg_extractor(redis_connection):
    return Extract(
        pg_settings=test_settings.pg.model_dump(),
        redis_connection=redis_connection,
        next_handler=lambda where_clause_table, pkeys: print(
            "Test Extract handler, with args:", where_clause_table, pkeys
        ),
    )


@pytest.fixture()
def pg_enricher(redis_connection):
    return Enricher(
        pg_settings=test_settings.pg.model_dump(),
        redis_connection=redis_connection,
        next_handler=lambda result: print("Test Enricher handler, with result:", result),
    )


@pytest.fixture(autouse=False)
def _clean_redis(redis_connection: Redis):
    with redis_connection as con:
        con.flushall()
