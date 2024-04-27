"""Extract data from source."""

import datetime
import logging
from collections.abc import Callable

from psycopg2.extensions import connection as _connection
from psycopg2.sql import SQL, Identifier
from redis import Redis
from psycopg2 import Error

from etl import sql_templates, state

logger = logging.getLogger(__name__)
import logging
import sqlite3
from dataclasses import astuple, dataclass, fields
from typing import Iterator


class Extractor:
    def __init__(self, connection: _connection, redis_settings: dict, result_handler: Callable):
        self.cursor = connection.cursor()
        self.result_handler = result_handler
        self.storage = state.RedisStorage(Redis(redis_settings))
        self.state = state.State(self.storage)

    def get_last_modified(self, table: str):
        modified = self.state.get_state(table)
        return modified or datetime.date.min

    def proccess(self, table: str, schema: str = "content", page_size: int = 100) -> None:
        query = SQL(sql_templates.get_modified_records).format(
            table=Identifier(schema, table),
        )
        self.cursor.execute(query, ({"modified": self.get_last_modified(table), "page_size": page_size}))
        query_result = self.cursor.fetchall()

        if query_result:
            modified = query_result[-1]["modified"]
            self.state.set_state(key=table, value=modified)
            self.result_handler(
                where_clause_table=table,
                pkeys=[record["id"] for record in query_result],
            )



class PostgresSaver:
    def __init__(self, connection: _connection, redis_connection: Redis):
        self.cursor = connection.cursor()
        self.storage = state.RedisStorage(redis_connection)
        self.state = state.State(self.storage)

    def get_last_modified(self, table: str):
        modified = self.state.get_state(table)
        return modified or datetime.date.min

    def get_table_data(self, table: str):
        query = f"SELECT * FROM content.{table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()



if __name__ == '__main__':
    from connectors import _pg_connection, PG_DSL
    with _pg_connection(PG_DSL) as pg_conn:
        PostgresSaver(pg_conn).get_table_data('genre')