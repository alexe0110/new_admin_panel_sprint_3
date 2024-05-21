import pytest
from redis import Redis

from components import Enricher, ESLoader, Extract, Transform
from config import Settings
from utils.state import RedisStorage

test_settings = Settings()


@pytest.fixture()
def redis_connection(redis_db: int | None):
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


@pytest.fixture()
def transformer(redis_connection):
    return Transform(
        redis_connection=redis_connection,
        next_handler=lambda movies_for_es: print("\nTest Transformer handler, with movies_for_es:", movies_for_es),
    )


@pytest.fixture()
def loader(redis_connection):
    return ESLoader(
        redis_connection=redis_connection,
        elastic_host=test_settings.es.addr,
        index=test_settings.es.index,
        schema=test_settings.es.index_schema,
    )


@pytest.fixture(autouse=False)
def _clean_redis(redis_connection: Redis):
    with redis_connection as con:
        con.flushall()
