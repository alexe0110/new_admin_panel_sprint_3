"""
Extract должен:
- читать данные пачками;
- спокойно переживать падение PostgreSQL;
- начинать читать с последней обработанной записи.
- сохранять в редис дату modified последней обработаной записи
"""

import datetime

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL
from redis import Redis

from mover.my_log import logger
from mover.state import RedisStorage, State
from mover.utils.sql_templates import get_modified_records


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
        query: SQL = SQL("select * from content.genre;")
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def get_last_modified(self, table: str):
        modified_date = self.state.get_state(table)
        if modified_date:
            return modified_date
        return datetime.date.min

    def extract_data(self, table: str, size: int = 100):
        query: SQL = SQL(get_modified_records.format(table=f"content.{table}"))

        self.cursor.execute(query)
