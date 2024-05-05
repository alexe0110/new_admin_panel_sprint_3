import pytest
from redis import Redis

from mover.config import Settings
from mover.state import RedisStorage

test_settings = Settings()


@pytest.fixture()
def storage() -> RedisStorage:
    return RedisStorage(Redis(**test_settings.redis_settings.model_dump()))


def test_state(storage: RedisStorage):
    storage.save_state({"kek": "lol"})
    red_res = storage.retrieve_state()
    assert red_res.get("kek") == "lol"
    print("red_res", red_res)
