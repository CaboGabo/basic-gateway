import os
from typing import List, Dict

from celery import Celery
from .cache.redis import save


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="fetch_query")
def fetch_query(query: str, hash: str, time: float):
    save(hash, {"hello": "world"})

    fetch_query.apply_async(
        kwargs={
            "query": query,
            "hash": hash,
            "time": time,
        },
        countdown=time,
    )


def delete_task(hash: str):
    workers: Dict[str, List[dict]] = celery.control.inspect().scheduled()

    for tasks in workers.values():
        for task in tasks:
            arguments: dict = task.get("kwargs", {})
            task_hash: str = arguments.get("hash", "")

            if hash != task_hash:
                continue

            request: dict = task.get("request", {})
            task_id = request.get("id", "")

            celery.control.revoke(task_id, terminate=True)


def purge_tasks():
    workers: Dict[str, List[dict]] = celery.control.inspect().scheduled()

    for tasks in workers.values():
        for task in tasks:
            request: dict = task.get("request", {})
            task_id = request.get("id", "")

            celery.control.revoke(task_id, terminate=True)
