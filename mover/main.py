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

from mover.components import Enricher, Extract, Transform
from mover.config import Settings
from mover.my_log import logger

settings = Settings()


def main():
    logger.info("Prepare to ETL")

    transform = Transform(
        redis_connection=Redis(**settings.redis_settings.model_dump(), db=2),
        next_handler=lambda movies_for_es: print(
            "Lambda func form main.py, если это текст появился Transform тригернулся на новую запись и "
            "превратил ее в объект для эластика:",
            len(movies_for_es),
            movies_for_es,
        ),
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

    while True:
        for table in settings.tables:
            extractor.extract_data(table)
            time.sleep(1)


if __name__ == "__main__":
    main()
