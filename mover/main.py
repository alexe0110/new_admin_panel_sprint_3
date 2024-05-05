"""
ETL состоит из 4х частей
    - Extract - вычитывает данные из БД
    - Enricher - обогащает данные  используя запрос get_movie_info_by_id
    - Transform - преобразует данные в формат для ES
    - Load - загружает данные в ES

Для каждой из частей есть кэширование в редисе
Настройки в config.py
"""
from mover.my_log import logger
from mover.config import Settings

settings = Settings()


def main():
    logger.info('Prepare to ETL')


if __name__ == '__main__':
    main()