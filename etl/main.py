import logging
from etl.extract import Extractor
from etl.config import Settings
from connectors import PG_DSL, _pg_connection

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('Prepare to start ETL')
    settings = Settings()

    extractor = Extractor(
        connection=_pg_connection(settings.postgres.model_dump()),   # todo не уверен сработает ли
        redis_connection=settings.redis_settings,
        result_handler=lambda x: print(x)
    )


    logger.info('Starting ETL')
    while True:
        for entity in settings.entities:
            extractor.extract_by_time(entity)

