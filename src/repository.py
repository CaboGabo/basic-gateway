from sqlalchemy.orm import Session
from . import models, schemas
from typing import Union


def get_query_by_id(db: Session, query_id: int):
    return db.query(models.Query).filter(models.Query.id == query_id).first()


def get_query_by_hash(db: Session, query_hash: str) -> Union[models.Query, None]:
    return db.query(models.Query).filter(models.Query.hash == query_hash).first()


def get_queries(db: Session):
    return db.query(models.Query).all()


def create_query(db: Session, query: schemas.QueryCreate):
    db_query = models.Query(
        query=query.query,
        time_to_execute_in_mins=query.time_to_execute_in_mins,
        hash=query.hash,
    )

    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    return db_query


def update_time_to_execute_in_mins(db: Session, db_query: models.Query, time: float):
    db_query.time_to_execute_in_mins = time
    db.commit()
    db.refresh(db_query)

    return db_query


def delete_query(db: Session, db_query: models.Query):
    db.delete(db_query)
    db.commit()
