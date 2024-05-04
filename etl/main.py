import logging

from connectors import _pg_connection
from redis import Redis

from etl.components.enricher import Enricher
from etl.components.extract import Extractor
from etl.components.load import ESLoader
from etl.components.transform import Transformer
from etl.config import Settings

logger = logging.getLogger(__name__)

settings = Settings()


def main(pg_conn):
    loader = ESLoader(
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=4),
        transport_options=settings.es.connection.dict(),
        index=settings.es.index,
        index_schema=settings.es.index_schema,
    )

    transformer = Transformer(
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=3),
        result_handler=loader.proccess,
    )

    enricher = Enricher(
        connection=pg_conn,
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=2),
        result_handler=transformer.proccess,
        page_size=settings.page_size,
    )

    extractor = Extractor(
        connection=pg_conn,  # todo не уверен сработает ли
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=1),
        result_handler=enricher.proccess,
    )

    for entity in settings.entities:
        extractor.extract_by_time(entity)


if __name__ == "__main__":
    logger.info("Starting ETL")

    while True:
        with _pg_connection(settings.postgres.model_dump()) as pg_connection:
            main(pg_connection)
