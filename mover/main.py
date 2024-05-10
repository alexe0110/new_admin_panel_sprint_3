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

from components.extract import Extract
from redis import Redis

from mover.config import Settings
from mover.my_log import logger

settings = Settings()


def main():
    logger.info("Prepare to ETL")

    extractor = Extract(
        pg_settings=settings.pg.model_dump(),
        redis_connection=Redis(**settings.redis_settings.model_dump()),
        next_handler=lambda where_clause_table, pkeys: print(
            "Lambda func form main.py, если это текст появился значит " "экстратор тригернулся на новую запись:",
            where_clause_table,
            pkeys,
        ),
    )

    while True:
        for table in settings.tables:
            extractor.extract_data(table)
            time.sleep(1)


if __name__ == "__main__":
    main()
