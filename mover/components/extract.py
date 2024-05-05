"""
Extract должен:
- читать данные пачками;
- спокойно переживать падение PostgreSQL;
- начинать читать с последней обработанной записи.
- сохранять в редис дату modified последней обработаной записи
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from redis import Redis

from mover.my_log import logger
from mover.state import RedisStorage, State


class Extract:
    def _connect(self) -> None:
        logger.debug(
            "Connecting to the DB %s. Timeout %s",
            self.pg_settings["dbname"],
            self.pg_settings["connect_timeout"],
        )
        self.connection = psycopg2.connect(**self.pg_settings)
        self.connection.set_session(readonly=True, autocommit=True)

        logger.debug("Connected to the DB %s", self.pg_settings["dbname"])

    def __init__(self, pg_settings: dict, redis_connection: Redis):
        self.pg_settings = pg_settings
        self._connect()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

    def kek(self):
        query = "select * from content.genre;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result
