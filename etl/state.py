import abc
import json
import logging
from typing import Any

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
        try:
            with open(self.file_path, "w") as wr_file:
                wr_file.write(data)
        except FileNotFoundError:
            logger.error(f"File {self.file_path} not found")

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, "r") as r_file:
                text = r_file.read()
        except FileNotFoundError:
            logger.error(f"File {self.file_path} not found")
            return {}

        states = json.loads(text)
        return states


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


if __name__ == '__main__':
    storage = JsonFileStorage("state.json")
    res=storage.retrieve_state()
    print(res)