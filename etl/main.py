import logging
from etl.extract import Extractor
from etl.config import Settings
from connectors import PG_DSL, _pg_connection
from redis import Redis
logger = logging.getLogger(__name__)

settings = Settings()

def main(conn):
    extractor = Extractor(
        connection=conn,  # todo не уверен сработает ли
        redis_connection=Redis(settings.redis_settings),
        result_handler=lambda x: print(x)
    )

    for entity in settings.entities:
        extractor.extract_by_time(entity)


if __name__ == '__main__':
    logger.info('Starting ETL')
    while True:
        with _pg_connection(settings.postgres.model_dump()) as pg_connection:
            main(pg_connection)
