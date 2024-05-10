from datetime import date, datetime

import pytest

from mover.components.extract import Extract
from mover.state import RedisStorage

#
# def test_extract_kek(pg_extractor: Extract):
#     res = pg_extractor.kek()
#
#     assert isinstance(res, list), f"Return not list, type = {type(res)}"
#     assert isinstance(res[0], RealDictRow), f"0 Element not RealDictRow, type = {type(res[0])}"


@pytest.mark.parametrize("table_name", ["film_work", "person", "genre"])
def test_extract_modified_date(pg_extractor: Extract, table_name: str):
    res = pg_extractor.get_last_modified(table=table_name)

    assert isinstance(res, date), "Last modified not date"


@pytest.mark.usefixtures("_clean_redis")
@pytest.mark.parametrize("table_name", ["film_work", "person", "genre"])
def test_extract_data(pg_extractor: Extract, redis_storage: RedisStorage, table_name: str):
    pg_extractor.extract_data(table=table_name)

    redis_res = redis_storage.retrieve_state()

    assert redis_res[table_name], "Not found in redis"
    assert isinstance(redis_res[table_name], datetime), "In redis not datetime"
