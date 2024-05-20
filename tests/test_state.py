import pytest

from utils.state import RedisStorage


@pytest.mark.parametrize("redis_db", [0])
def test_state(redis_storage: RedisStorage):
    redis_storage.save_state({"kek": "lol"})
    red_res = redis_storage.retrieve_state()

    assert red_res.get("kek") == "lol", f"State not lol, state = {red_res.get('kek')}"
