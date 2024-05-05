"""
Extract должен:
- читать данные пачками;
- спокойно переживать падение PostgreSQL;
- начинать читать с последней обработанной записи.
- сохранять в редис дату modified последней обработаной записи
"""
import logging
from redis import Redis
from mover.my_log import logger
import psycopg2


class Extract:
    def _connect(self) -> None:
        """PG connection function with backoff wrapper."""
        logger.debug(
            'Connecting to the DB %s. Timeout %s',
            self.pg_settings['dbname'],
            self.pg_settings['connect_timeout'],
        )
        self.connection = psycopg2.connect(**self.pg_settings)
        self.connection.set_session(readonly=True, autocommit=True)

        logger.debug('Connected to the DB %s', self.pg_settings['dbname'])

    def __init__(self, pg_settings: dict):
        self.pg_settings = pg_settings
        self._connect()


if __name__ == '__main__':
    ex = Extract()