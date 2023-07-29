from typing import Optional, List

from pydantic import BaseModel


class MovieData(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Actor(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Category(MovieData):
    pass


class Series(MovieData):
    pass


class Studio(MovieData):
    pass


class MovieBase(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode=True

class MovieProperty(BaseModel):
    name: str

class MovieFile(MovieBase):
    pass


class Movie(MovieBase):
    name: Optional[str]
    actors: Optional[List[Actor]] = None
    categories: Optional[List[Category]] = None
    series: Optional[Series] = None
    series_number: Optional[int] = None
    studio: Optional[Studio] = None

    class Config:
        orm_mode = True

class HTTPExceptionMessage(BaseModel):
    message:str

class MovieUpdateSchema(BaseModel):
    name: Optional[str] = None
    series_id: Optional[int] = None
    series_number: Optional[int] = None
    studio_id: Optional[int] = None

