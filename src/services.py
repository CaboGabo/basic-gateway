import hashlib
import json
from . import schemas, repository
from .worker import fetch_query, delete_task, purge_tasks

from .cache.redis import get_data


def get_queries(db):
    return repository.get_queries(db)


def hash_query(hash: str) -> str:
    return hashlib.md5(hash.encode()).hexdigest()


def create_query(db, query: schemas.QueryCreate):
    query.hash = hash_query(query.query)

    query_with_same_hash = repository.get_query_by_hash(db, query.hash)

    if query_with_same_hash:
        if (
            query_with_same_hash.time_to_execute_in_mins
            == query.time_to_execute_in_mins
        ):
            return query_with_same_hash

        db_query = repository.update_time_to_execute_in_mins(
            db, query_with_same_hash, query.time_to_execute_in_mins
        )

        delete_task(query.hash)
        send_query(query)

        return db_query

    db_query = repository.create_query(db, query)
    send_query(query)

    return db_query


def delete_query_by_hash(db, hash: str):
    db_query = repository.get_query_by_hash(db, hash)

    if not db_query:
        return

    repository.delete_query(db, db_query)
    delete_task(hash)
    return db_query


def send_query(query: schemas.QueryCreate):
    time = query.time_to_execute_in_mins
    fetch_query.apply_async(
        kwargs={
            "query": query.query,
            "hash": query.hash,
            "time": query.time_to_execute_in_mins,
        },
        countdown=time,
    )  # Using seconds instead of minutes for testing purposes


def get_query_data(query: schemas.QueryCreate):
    hash = hash_query(query.query)
    return get_data(hash)


def purge_all_tasks():
    purge_tasks()
