"""
Extract должен:
- читать данные пачками;
- спокойно переживать падение PostgreSQL;
- начинать читать с последней обработанной записи. путем сохранения modified в редис
- сохранять в редис дату modified последней обработаной записи
"""

import datetime
from collections.abc import Callable

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier
from redis import Redis

from utils.logger import logger
from utils.sql_templates import get_modified_records
from utils.state import RedisStorage, State


class Extract:
    def _connect(self) -> None:
        self.connection = psycopg2.connect(**self.pg_settings)
        self.connection.set_session(readonly=True, autocommit=True)

        logger.debug(f"Extract connect to db {self.pg_settings['dbname']}")

    def __init__(self, pg_settings: dict, redis_connection: Redis, next_handler: Callable):
        self.pg_settings = pg_settings
        self._connect()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.next_handler = next_handler

    def get_last_modified(self, table: str) -> datetime.date:
        modified_date = self.state.get_state(table)

        if modified_date:
            return modified_date
        return datetime.date.min

    def extract_data(self, table: str, schema: str = "content", size: int = 100) -> None:
        logger.debug(f"Getting data from {table}")

        query = SQL(get_modified_records).format(
            table=Identifier(schema, table),
        )

        self.cursor.execute(query, {"modified": self.get_last_modified(table), "page_size": size})
        result = self.cursor.fetchall()

        if result:
            logger.info(f'Detect modified records{result}')

            modified = result[-1]["modified"]
            self.state.set_state(key=table, value=modified)
            self.next_handler(
                where_clause_table=table,
                pkeys=[record["id"] for record in result],
            )
