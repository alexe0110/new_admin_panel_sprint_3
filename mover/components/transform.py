"""
Transform преобразует данные полученные из БД к формату, который может быть записан в эластик
"""

from collections.abc import Callable

import psycopg2
from psycopg2.sql import SQL, Identifier
from redis import Redis

from mover.my_log import logger
from mover.state import RedisStorage, State
from mover.utils.sql_templates import get_movie_info_by_id
from psycopg2.extras import RealDictRow
from mover.es_models import Movie, Person


class Transform:
    def __init__(self, redis_connection: Redis, next_handler: Callable):
        self.storage = RedisStorage(redis_connection)
        self.state = State(self.storage)

        self.next_handler=next_handler
        self.proceed()

    def proceed(self) -> None:
        """
        Проверяет данные в редисе по ключу data, есть ли там данные из БД
        вида `[RealDictRow([('id', 'a9b29ca3-adf2-46b9-8455-9dccda64c400'), ('imdb_rating', 6.0),...`
        Если есть, то отправляет их на переработку в данне для эластика методу transform_data
        """
        if self.state.state.get('data'):
            logger.debug('Data to proceed %s', self.state.state.get('data'))
            self.transform_data(
                movies=self.state.state.get('data')
            )

    def get_person_names(self, persons: dict, role: str|None = None) -> list:
        """
        Получение всех имен персонажей указанной роли
        """

        if role:
            return [person['name'] for person in persons if person['role'] == role]
        else:
            return [person['name'] for person in persons]

    def persons_by_role(self, persons, role: str|None = None) -> list:
        if role:
            return [Person(**person).dict() for person in persons if person['role'] == role]
        else:
            return [Person(**person).dict() for person in persons]

    def set_state(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.state.set_state(key=key, value=value)

    def transform_data(self, movies: list[RealDictRow]) -> None:
        """
        Основной метод, преобразует данные из  `[RealDictRow([('id', 'a64c400'), ('imdb_rating', 6.0),...`
        в данные для эластика
        Может вызваться Enricherом или из метода proceed

        :param movies: список данных из БД
        """
        self.set_state(data=movies)
        movies_for_es = []

        for movie_id, movie in enumerate(movies):
            try:
                movies_for_es.append(
                    Movie(
                        **movie,
                        directors_names=self.get_person_names(movie['persons'], 'director'),
                        actors_names=self.get_person_names(movie['persons'], 'actor'),
                        writers_names=self.get_person_names(movie['persons'], 'writer'),
                        directors=self.persons_by_role(movie['persons'], 'director'),
                        actors=self.persons_by_role(movie['persons'], 'actor'),
                        writers=self.persons_by_role(movie['persons'], 'writer'),
                    ).dict(by_alias=True)
                )

            except ValueError:
                logger.exception(f'Error in transform_data {movie}')

        self.set_state(data=None)   # Чтобы в кэше было чисто и при следующем запуске proceed не пыталась записать то, что уже записано
        self.next_handler(movies_for_es)
