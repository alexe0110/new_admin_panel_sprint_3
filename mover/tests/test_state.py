from mover.state import RedisStorage


def test_state(redis_storage: RedisStorage):
    redis_storage.save_state({"kek": "lol"})
    red_res = redis_storage.retrieve_state()

    assert red_res.get("kek") == "lol", f"State not lol, state = {red_res.get('kek')}"
