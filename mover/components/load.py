"""
ESLoader должен
    - загружать данные пачками;
    - без потерь переживать падение Elasticsearch;
    - принимать/формировать поле, которое будет считаться id в Elasticsearch.

Вид записи в эластик:

"""

from elasticsearch import Elasticsearch
from redis import Redis

from mover.state import RedisStorage, State


class ESLoader:
    def __init__(self, redis_connection: Redis, elastic_settings: dict, index: str, schema: dict = None):
        self.es_client = Elasticsearch(**elastic_settings)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.index = index

    def bulk_upload(self, data: list):
        pass
