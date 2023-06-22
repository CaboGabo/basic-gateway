import redis
import json

redis_conn = redis.Redis(host="redis", port=6379)


def save(key: str, value: dict):
    parsed_value = json.dumps(value)
    redis_conn.set(key, parsed_value)


def get_data(key: str):
    data = redis_conn.get(key)

    if not data:
        return

    return json.loads(data.decode())
