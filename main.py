from os.path import splitext
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

import crud
import schemas
from database import Base, engine, SessionLocal, get_db
import models
from config import get_config
from util import list_files

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

config = get_config()


@app.get('/')
def hello():
    return {"hello": "world"}


@app.post('/import_movies', response_model=List[schemas.Movie])
def import_movies(db: Session = Depends(get_db)):
    try:
        files = list_files(config['imports'])
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': str(e)}
        )
    movies = []
    for file in files:
        name, _ = splitext(file)
        movie = crud.add_movie(db, file, name)
        if movie is not None:
            movies.append(movie)

    return movies


@app.get('/movies', response_model=List[schemas.MovieFile])
async def get_movies(db: Session = Depends(get_db)):
    return crud.get_all_movies(db)


@app.post("/actors", response_model=schemas.Actor)
async def add_actor(data: schemas.MovieProperty, db: Session = Depends(get_db)):
    actor = crud.add_actor(db, data.name)
    if actor is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={'message': f'Actor {data.name} already in database'}
                            )
    return actor


@app.get('/actors', response_model=List[schemas.Actor])
async def get_actors(db: Session = Depends(get_db)):
    return crud.get_all_actors(db)


@app.get('/movies/{id}', response_model=schemas.Movie, responses={404: {
    'model': schemas.HTTPExceptionMessage,
    'description': 'invalid id'
}})
async def get_movie(id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, id)
    if movie is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail={'message': f'movie dont exist /gang'}
                            )
    return movie


@app.put('/movies/{id}', response_model=schemas.Movie, responses={404: {
    'model': schemas.HTTPExceptionMessage,
    'description': 'invalid id'}})
async def update_movie_data(id: int, data: schemas.MovieUpdateSchema, db: Session = Depends(get_db)):
    movie = crud.update_movie(db, id, data)
    if movie is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={'error /gang'}
                            )
    return movie


@app.post('/movie_category', response_model=schemas.Movie, responses={404: {
    'model': schemas.HTTPExceptionMessage,
    'description': 'invalid id'}})
async def add_movie_category(movie_id: int, category_id: int, db: Session = Depends(get_db)):
    movie = crud.add_movie_category(movie_id, category_id, db)
    if movie is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={'error /gang'}
                            )
    return movie


