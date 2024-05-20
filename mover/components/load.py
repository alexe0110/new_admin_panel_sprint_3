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

from elasticsearch import Elasticsearch
from redis import Redis

from mover.state import RedisStorage, State

from collections.abc import Callable
from elasticsearch.helpers import bulk

from psycopg2.extras import RealDictRow
from redis import Redis

from mover.es_models import Movie, Person
from mover.my_log import logger
from mover.state import RedisStorage, State


class ESLoader:
    def __init__(self, redis_connection: Redis, elastic_host: str, index: str, schema: dict = None):
        self.es_client = Elasticsearch(elastic_host)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.index = index

        # self.proceed()

    def proceed_by_cache(self):
        if data_cache := self.state.state.get('data'):
            logger.debug(f'Proceed by cache: {data_cache}')
            self.bulk_upload(data_cache)

    def convert_to_bulk_format(self, data: dict) -> dict:
        pass

    def bulk_upload(self, data: list[dict]):
        """
        Метода для загрузки данных в ES в булк формате.
        """
        logger.debug(f'Bulk upload: {data}')
        result = bulk(self.es_client, data, index=self.index)
        print('\tResult:', result)

    def process(self, data: dict):
        """
        Подготовка данных для загрузки в ES: сохранение в редис и перевод в булк формат,
        с последующей передачей в метод bulk_upload
        """
        self.state.set_state(key='data', value=data)
        print('\t data to load', data)
        # bulk_data = []
        # self.bulk_upload(data)