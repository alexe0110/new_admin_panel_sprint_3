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
    def __init__(self, connection: _connection, redis_connection: Redis, result_handler: Callable):
        self.cursor = connection.cursor()
        self.result_handler = result_handler
        self.storage = state.RedisStorage(redis_connection)
        self.state = state.State(self.storage)

    def get_last_modified(self, table: str):
        modified = self.state.get_state(table)
        return modified or datetime.date.min

    def get_table_data(self, table: str):
        query = f"SELECT * FROM content.{table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def extract_by_time(self, table: str, schema: str = "content", page_size: int = 100):
        query = SQL(sql_templates.get_modified_records).format(
            table=Identifier(schema, table),
        )

        self.cursor.execute(query, {"modified": self.get_last_modified(table), "page_size": page_size})
        result = self.cursor.fetchall()
        if result:
            modified = result[-1]['modified']
            self.state.set_state(key=table, value=modified)
            # todo: Разобраться зачем
            self.result_handler(
                where_clause_table=table,
                pkeys=[record['id'] for record in result],
            )

        return result


if __name__ == '__main__':
    from connectors import _pg_connection, PG_DSL
    with _pg_connection(PG_DSL) as pg_conn:
        # PostgresSaver(pg_conn).get_table_data('genre')
        # PostgresSaver(pg_conn, Redis(host='localhost', port=6379)).get_last_modified('genre')
        res = Extractor(pg_conn, Redis(host='localhost', port=6379), result_handler=lambda where_clause_table, pkeys: print(where_clause_table, pkeys)).extract_by_time(table='genre')
        print(res)
    #
    #
    # query = SQL(sql_templates.get_modified_records)
    # print(query)
    # schema: str = "content"
    # table: str = "genre"
    # query2 = query.format(
    #         table=Identifier(schema, table),
    #     )
    # print(query2)
    #
