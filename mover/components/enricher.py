"""
Enricher добавляет инфу о фильме и передает результат дальше
"""

from collections.abc import Callable

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier
from redis import Redis

from mover.my_log import logger
from mover.state import RedisStorage, State
from mover.utils.sql_templates import get_movie_info_by_id


class Enricher:
    def _connect(self) -> None:
        logger.debug(
            "Enricher connecting to the DB %s. Timeout %s",
            self.pg_settings["dbname"],
            self.pg_settings["connect_timeout"],
        )
        self.connection = psycopg2.connect(**self.pg_settings)
        self.connection.set_session(readonly=True, autocommit=True)

        logger.debug("Enricher connected to the DB %s", self.pg_settings["dbname"])

    def __init__(self, pg_settings: dict, redis_connection: Redis, next_handler: Callable, size: int = 100):
        self.pg_settings = pg_settings
        self._connect()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.next_handler = next_handler
        self.size = size

        self.proceed()

    def proceed(self) -> None:
        if self.state.state.get("pkeys"):
            logger.debug("Data to proceed %s", self.state.state.get("pkeys"))
            self.enrich_data(
                self.state.state['table'],
                self.state.state['pkeys']
            )

    def set_state(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.state.set_state(key=key, value=value)

    def enrich_data(self, where_clause_table: str, pkeys: list) -> None:
        query = SQL(get_movie_info_by_id).format(where_clause_table=Identifier(where_clause_table))

        self.cursor.execute(
            query,
            {"pkeys": tuple(pkeys), "last_id": self.state.get_state("last_processed_id") or "", "page_size": self.size},
        )

        while result := self.cursor.fetchall():
            self.set_state(
                table=where_clause_table,
                pkeys=pkeys,
                last_processed_id=result[-1]["id"],
                page_size=self.size,
            )

            logger.debug("Got additional info for %s  movies", len(result))
            self.next_handler(result)

        self.set_state(
            table=None,
            pkeys=None,
            last_processed_id=None,
            page_size=None,
        )
