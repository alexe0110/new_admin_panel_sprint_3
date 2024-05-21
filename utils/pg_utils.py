import backoff
import psycopg2

from utils.logger import logger


class PGConnection:
    @backoff.on_exception(lambda: backoff.expo(base=2, factor=0.1), Exception, max_time=10)
    def _connect(self, pg_settings: dict) -> None:
        logger.info(f"Try connect to db {pg_settings['dbname']}")

        self.connection = psycopg2.connect(**pg_settings)
        self.connection.set_session(readonly=True, autocommit=True)

        logger.info(f"{self.__class__} success connect to db {pg_settings['dbname']}")
