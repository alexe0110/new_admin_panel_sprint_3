import abc
import logging
import pickle
from typing import Any

from redis import Redis

logger = logging.getLogger(__name__)


class BaseStorage(abc.ABC):
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis) -> None:
        self.redis_adapter = redis_adapter

    def save_state(self, state: dict) -> None:
        for key, value in state.items():
            self.redis_adapter.set(name=key, value=pickle.dumps(value))

    def retrieve_state(self) -> dict:
        state = {}
        keys = self.redis_adapter.keys()
        for key in keys:
            value = self.redis_adapter.get(key)
            state[key.decode("utf-8")] = pickle.loads(value)

        return state


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self.state = self.storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        self.storage.save_state(state={key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        return self.storage.retrieve_state().get(key)


if __name__ == "__main__":
    red_storage = RedisStorage(Redis(host="localhost", port=6379))
    red_res = red_storage.retrieve_state()
    print(red_res)
