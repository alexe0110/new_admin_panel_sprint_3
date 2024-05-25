"""
ESLoader должен
    - загружать данные пачками;
    - без потерь переживать падение Elasticsearch;
    - принимать/формировать поле, которое будет считаться id в Elasticsearch.

Вид записи в эластик:
    # [{'id': 'a9b29ca3-adf2-46b9-8455-9dccda64c400', 'imdb_rating': 6.0, 'genre': [None], 'title': 'Sunday Kek',
    # 'description': 'qweqweqwe', 'directors_names': [], 'actors_names': [], 'writers_names': [], 'directors': [],
    # 'actors': [], 'writers': []}, {'id': 'a9b29ca3-adf2-46b9-8455-9dccda64c402', 'imdb_rating': 8.0,
    # 'genre': ['News7'],'title': 'Sunday Haha', 'description': 'ahahahahha', 'directors_names': [],
    # 'actors_names': ['George Lucas'], 'writers_names': [], 'directors': [], 'actors': [{
    # 'id': 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', 'name': 'George Lucas'}], 'writers': []}]
"""

from elastic_transport import ConnectionError, ConnectionTimeout
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from redis import Redis

from utils.logger import logger
from utils.my_backoff import backoff
from utils.state import RedisStorage, State


class ESLoader:
    def __init__(self, redis_connection: Redis, elastic_host: str, index: str, schema: dict):
        self.es_client = Elasticsearch(elastic_host)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.index = index

        self.create_index(index, schema)
        self.proceed_by_cache()

    @backoff(exceptions=(ConnectionTimeout, ConnectionError))
    def create_index(self, index: str, schema: dict) -> None:
        if not self.es_client.indices.exists(index=index):
            logger.info(f"Index {index} not exists. Creating new one")
            self.es_client.indices.create(index=index, body=schema)

    def proceed_by_cache(self):
        if data_cache := self.state.state.get("data"):
            logger.debug(f"Proceed by cache: {data_cache}")
            self.bulk_upload(data_cache)

    def convert_to_bulk(self, data: dict) -> dict:
        return {"_id": data.get("id"), "_index": self.index, "_source": data}

    @backoff(exceptions=(ConnectionTimeout, ConnectionError))
    def bulk_upload(self, data: dict):
        """
        Метода для загрузки данных в ES в булк формате.
        """
        logger.debug(f"Bulk upload: {len(data)}")

        self.state.set_state(key="data", value=data)
        bulk_data = [self.convert_to_bulk(i) for i in data]

        try:
            bulk(self.es_client, bulk_data, index=self.index)
        except Exception as e:
            logger.exception("Error during bulk upload")
            raise e

        self.state.set_state(key="data", value=None)
