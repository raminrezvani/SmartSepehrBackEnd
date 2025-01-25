import json

from redis import Redis

redis_connection = Redis(host="redis")


def add_dict_to_redis(key: str, value: dict, **kwargs) -> bool:
    """
    add dict with particular key into redis
    :param key: redis key
    :param value: dict
    :return: bool => True => add, False => couldn't add
    """
    try:
        redis_connection.set(key, json.dumps(value), **kwargs)
        return True
    except:
        return False


def check_redis_key(key: str) -> bool:
    """
    check if redis has the key or not
    :param key: redis key
    :return: bool => True => this key exists in redis
    """
    return bool(redis_connection.exists(key))


def get_dict_from_redis(key: str) -> [dict, list]:
    """
    get dict or list from redis by key
    :param key: redis key
    :return: dict or list
    """
    try:
        return json.loads(redis_connection.get(key))
    except:
        return {}


def delete_key_redis(key: str) -> bool:
    """
    delete key and value from redis
    :param key: redis key
    :return: True ==> successfully deleted
    """
    try:
        redis_connection.delete(key)
        return True
    except:
        return False
