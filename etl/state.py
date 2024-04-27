import abc
import json
import logging
import pickle
from collections.abc import Callable
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


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        data = json.dumps(state, indent=4, sort_keys=True, default=str)
        with open(self.file_path, "w") as wr_file:
            wr_file.write(data)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path) as r_file:
                text = r_file.read()
        except FileNotFoundError:
            logger.error(f"File {self.file_path} not found")
            return {}

        states = json.loads(text)
        return states


class RedisStorage(BaseStorage):
    def __init__(self, connection_settings: dict) -> None:
        """RedisStorage class constructor.

        Args:
            dict: storage connection settings.

        """
        self.connection_settings = connection_settings
        self._connect()

    # @backoff()
    def _connect(self):
        self.redis_adapter = Redis(**self.connection_settings)
        self.redis_adapter.ping()

    # @backoff_reconnect()
    def try_command(self, func: Callable, *args, **kwargs) -> Any:
        return func(*args, **kwargs)

    def save_state(self, state: dict) -> None:
        for key, value in state.items():
            self.try_command(self.redis_adapter.set, name=key, value=pickle.dumps(value))

    def retrieve_state(self) -> dict:
        state = {}
        keys = self.try_command(self.redis_adapter.keys, "*")
        for key in keys:
            value = self.try_command(self.redis_adapter.get, key)
            try:
                state[key.decode("utf-8")] = pickle.loads(value)
            except pickle.UnpicklingError:
                state[key.decode("utf-8")] = value.decode("utf-8") if value else None
        return state


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        self.storage.save_state(state={key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        return self.storage.retrieve_state().get(key)


if __name__ == "__main__":
    storage = JsonFileStorage("state.json")
    res = storage.retrieve_state()
    storage.save_state({"dsa": "dsadsdd"})
    print(res)
    print("======================================================")

    red_storage = RedisStorage(connection_settings={"host": "localhost", "port": 6379})
    red_storage.save_state({"kek": "lol"})
    red_res = red_storage.retrieve_state()
    print(red_res)
