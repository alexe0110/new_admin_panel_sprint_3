import datetime

import pytest
from psycopg2.extras import RealDictRow

from components import Transform
from utils.state import RedisStorage

test_data = [
    RealDictRow(
        [
            ("id", "a9b29ca3-adf2-46b9-8455-9dccda64c400"),
            ("imdb_rating", 6.0),
            ("title", "Sunday Kek"),
            ("description", "qweqweqwe"),
            ("modified", datetime.datetime(2024, 5, 5, 12, 30, 11, 778838, tzinfo=datetime.UTC)),
            ("persons", []),
            ("genre", [None]),
        ]
    ),
    RealDictRow(
        [
            ("id", "a9b29ca3-adf2-46b9-8455-9dccda64c402"),
            ("imdb_rating", 8.0),
            ("title", "Sunday Haha"),
            ("description", "ahahahahha"),
            ("modified", datetime.datetime(2024, 5, 5, 17, 21, 11, 778838, tzinfo=datetime.UTC)),
            ("persons", [{"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas", "role": "actor"}]),
            ("genre", ["News7"]),
        ]
    ),
]


@pytest.mark.parametrize("redis_db", [2])
def test_transform_data(transformer: Transform, redis_storage: RedisStorage, redis_db: int):
    transformer.transform_data(test_data)
    redis_result = redis_storage.retrieve_state()

    assert (
        redis_result["data"] is None
    ), '"data" должен создаться в редисе, хоть останется пустым после выоплненяи трансформ'
