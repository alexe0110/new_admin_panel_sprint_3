from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: str
    imdb_rating: float | None
    genre: list[str]
    title: str
    description: str | None
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[Person] | None
    writers: list[Person] | None

    class Config:
        populate_by_name = True
