import pytest

from mover.components import Transform
from mover.state import RedisStorage


@pytest.mark.kek()
@pytest.mark.parametrize("redis_db", [2])
def test_transform_data(transformer: Transform, redis_storage: RedisStorage, redis_db: int):
    pass
