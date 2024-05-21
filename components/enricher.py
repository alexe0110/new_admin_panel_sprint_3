"""
Enricher добавляет инфу о фильме и передает результат дальше
"""

from collections.abc import Callable

from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Identifier
from redis import Redis

from utils.logger import logger
from utils.pg_utils import PGConnection
from utils.sql_templates import get_additional_info
from utils.state import RedisStorage, State


class Enricher(PGConnection):
    def __init__(self, pg_settings: dict, redis_connection: Redis, next_handler: Callable, size: int = 100):
        self.pg_settings = pg_settings
        self._connect(pg_settings)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.next_handler = next_handler
        self.size = size

        self.proceed()

    def proceed(self) -> None:
        if data_cache := self.state.state.get("pkeys"):
            logger.debug(f"Proceed by cache: {data_cache}")
            self.enrich_data(self.state.state["table"], self.state.state["pkeys"])

    def set_state(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.state.set_state(key=key, value=value)

    def enrich_data(self, where_clause_table: str, pkeys: list) -> None:
        query = SQL(get_additional_info).format(where_clause_table=Identifier(where_clause_table))

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

            logger.debug(f"Enrich data for {len(result)}  movies")
            self.next_handler(result)

        self.set_state(
            table=None,
            pkeys=None,
            last_processed_id=None,
            page_size=None,
        )
