"""
ETL состоит из 4х частей
    - Extract - вычитывает данные из БД
    - Enricher - обогащает данные  используя запрос get_movie_info_by_id
    - Transform - преобразует данные в формат для ES
    - Load - загружает данные в ES

Для каждой из частей есть кэширование в редисе
Настройки в config.py
"""

import time

from redis import Redis

from components import Enricher, ESLoader, Extract, Transform
from config import Settings
from utils.logger import logger

settings = Settings()


def main():
    logger.info("Prepare to ETL")

    loader = ESLoader(
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=3),
        elastic_host=settings.es.addr,
        index=settings.es.index,
        schema=settings.es.index_schema,
    )

    transform = Transform(
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=2),
        next_handler=loader.bulk_upload,
    )

    enricher = Enricher(
        pg_settings=settings.pg.model_dump(),
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=1),
        next_handler=transform.transform_data,
    )

    extractor = Extract(
        pg_settings=settings.pg.model_dump(),
        redis_connection=Redis(**settings.redis_settings.model_dump()),
        next_handler=enricher.enrich_data,
    )

    logger.info("Start consume")
    while True:
        for table in settings.tables:
            extractor.extract_data(table)
            time.sleep(settings.delay)


if __name__ == "__main__":
    main()
