import logging
from etl.components.extract import Extractor
from etl.components.enricher import Enricher
from etl.config import Settings
from connectors import _pg_connection
from redis import Redis
logger = logging.getLogger(__name__)

settings = Settings()


def main(pg_conn):

    # transformer = Transformer(
    #     redis_settings=settings.cache.transformer,
    #     result_handler=loader.proccess,
    # )

    enricher = Enricher(
        connection=pg_conn,
        redis_connection=Redis(**settings.redis_settings.model_dump()),
        result_handler=transformer.proccess,
        page_size=settings.page_size,
    )

    extractor = Extractor(
        connection=pg_conn,  # todo не уверен сработает ли
        redis_connection=Redis(**settings.redis_settings.model_dump()),
        result_handler=enricher.proccess
    )

    for entity in settings.entities:
        extractor.extract_by_time(entity)


if __name__ == '__main__':
    logger.info('Starting ETL')

    while True:
        with _pg_connection(settings.postgres.model_dump()) as pg_connection:
            main(pg_connection)
