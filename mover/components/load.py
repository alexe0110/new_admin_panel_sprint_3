"""
ESLoader должен
    - загружать данные пачками;
    - без потерь переживать падение Elasticsearch;
    - принимать/формировать поле, которое будет считаться id в Elasticsearch.

Вид записи в эластик:

"""


import datetime
from collections.abc import Callable

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier
from redis import Redis
from elasticsearch import Elasticsearch, helpers

from mover.my_log import logger
from mover.state import RedisStorage, State
from mover.utils.sql_templates import get_modified_records


class ESLoader:
    def __init__(self, redis_connection: Redis, elastic_settings: dict, index: str, schema: dict=None):
        self.es_client = Elasticsearch(**elastic_settings)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.index = index

    def bulk_upload(self, data: list):
        pass
