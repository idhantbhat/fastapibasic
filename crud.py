from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import models
import schemas
import util


def add_actor(
        db: Session,
        name: str
) -> models.Actor:
    actor = models.Actor(
        name=name
    )
    try:
        db.add(actor)
        db.commit()
        db.refresh(actor)
    except IntegrityError:
        db.rollback()
        return None
    return actor


def add_movie(
        db: Session,
        filename: str,
        name: str,
        studio_id: Optional[int] = None,
        series_id: Optional[int] = None,
        series_number: Optional[int] = None,
        actor_ids: Optional[List[int]] = None,
        category_ids: Optional[List[int]] = None,
        processed: Optional[bool] = False
) -> models.Movie:
    movie = models.Movie(
        filename=filename,
        name=name,
        studio_id=studio_id,
        series_id=series_id,
        series_number=series_number,
        processed=processed
    )

    if actor_ids is not None:
        movie.actors = actor_ids
    if category_ids is not None:
        movie.categories = category_ids

    try:
        db.add(movie)
        db.commit()
        db.refresh(movie)
    except IntegrityError:
        db.rollback()
        return None

    util.migrate_files(movie)
    return movie


def get_all_movies(db: Session) -> List[models.Movie]:
    return (
        db.query(models.Movie).outerjoin(models.Studio).outerjoin(models.Series).order_by(models.Movie.processed,
                                                                                          models.Studio.name,
                                                                                          models.Series.name,
                                                                                          models.Movie.name).all()
    )

def get_movie(db: Session, id: int) -> models.Movie:
    return (
        db.query(models.Movie).filter(models.Movie.id == id).first()
    )

def get_category(db: Session, id: int) -> models.Category :
    return (
        db.query(models.Category).filter(models.Category.id == id).first()
    )

def get_all_actors(db: Session) -> List[models.Actor]:
    return (
        db.query(models.Actor).order_by(models.Actor.name,).all()
    )

def update_movie(db:Session, id:int, data: schemas.MovieUpdateSchema) ->models.Movie:
    movie = get_movie(db, id)
    if movie is None:
        return None
    if data.name == movie.name and data.studio_id == movie.studio_id and data.series_id == movie.series_id and data.series_number == movie.series_number:
        return movie
    movie.name = data.name
    movie.series_id = data.series_id
    movie.series_number = data.series_number
    movie.studio_id = data.studio_id
    if not movie.processed:
        movie.processed == True
    db.commit()
    db.refresh(movie)
    return movie

def add_movie_category(movie_id:int, category_id: int, db:Session) -> models.Movie:
    movie = get_movie(db, movie_id)
    category = get_category(db, category_id)
    if movie is None or category is None:
        return None
    movie.categories.append(category)
    db.commit()
    db.refresh(movie)
    return movie