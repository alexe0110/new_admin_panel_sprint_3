from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: str
    imdb_rating: float | None
    genre: list[str | None]
    title: str
    description: str | None
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[Person] | None
    actors: list[Person] | None
    writers: list[Person] | None
