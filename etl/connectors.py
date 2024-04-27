import os
import sqlite3
from contextlib import contextmanager
from typing import Type

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor, DictCursorBase

load_dotenv()

PG_DSL = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}



@contextmanager
def _pg_connection(dsl: dict[str | str], custom_cursor_factory: Type[DictCursorBase] = DictCursor):
    conn = psycopg2.connect(**dsl, cursor_factory=custom_cursor_factory)

    try:
        yield conn
    finally:
        conn.commit()
