import json
from requests import request

#BASE_URL = "http://94.74.182.183:6886/"
BASE_URL = "http://localhost:6886/"

def has_key_cache(key: str) -> bool:
    """
    check if key has cache or not
    :param key: key
    :return: True => key has cache
    """
    try:
        url = BASE_URL + "has-cache"
        body = {
            "key": key
        }
        # ---
        req = request("POST", url, json=body)
        data = json.loads(req.text)
        # ---
        return data['has']
    except:
        return False


def get_cache(key: str, get_time: bool = False) -> [list, dict]:
    """
    get cache data
    :param key: key
    :param get_time: get time of created
    :return: everything is in cache with the key
    """
    try:
        # ---
        url = BASE_URL + 'get-cache'
        body = {
            "key": key,
            "get_time": get_time
        }
        # ---
        req = request("POST", url, json=body)
        data = json.loads(req.text)
        # ---
        return data
    except:
        return []


def add_cache(key: str, data: [list, dict]) -> bool:
    """
    add data to cache
    :param key: key
    :param data: data
    :return: True => data saved in cache, False => data cannot save in cache
    """
    try:
        # ---
        url = BASE_URL + "add-cache"
        body = {
            "key": key,
            "data": data
        }
        # ---
        req = request("POST", url, json=body)
        data = json.loads(req.text)
        # ---
        return data['add']
    except:
        return False
