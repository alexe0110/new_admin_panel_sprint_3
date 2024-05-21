import psycopg2
from psycopg2 import OperationalError

from utils.logger import logger
from utils.my_backoff import backoff


class PGConnection:
    @backoff(exceptions=(OperationalError,))
    def _connect(self, pg_settings: dict) -> None:
        logger.info(f"Try connect to db {pg_settings['dbname']}")

        try:
            self.connection = psycopg2.connect(**pg_settings)
            self.connection.set_session(readonly=True, autocommit=True)
        except OperationalError as e:
            logger.error(f"Failed connect {self.__class__} to db {pg_settings['dbname']}")
            raise e

        logger.info(f"Success connect {self.__class__}  to db {pg_settings['dbname']}")
