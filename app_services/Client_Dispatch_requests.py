import requests
import json
import redis
from itertools import cycle
import hashlib

# SSH smartland@185.252.28.58 -p 2858
# Initialize Redis connection

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# Define servers and ports
servers = [


    # ("130.185.77.24", [6000, 6001, 6002, 6003, 6004, 6005]),
    ("45.149.76.168", [6000, 6001, 6002, 6003, 6004, 6005]),
    ("185.252.28.58", [6000, 6001, 6002, 6003, 6004, 6005]),
    # ("185.252.30.120", [6000, 6001, 6002, 6003, 6004, 6005]),

]

# Round-robin cycle for selecting servers
server_cycle = cycle([server for server, _ in servers])

# Dictionary to store which server is assigned to each priorityTimestamp
timestamp_server_map = {}

# Dictionary to store round-robin port selection for each server
server_port_cycles = {
    server: cycle(ports) for server, ports in servers
}


def get_cache_key(method, url, params, cookies, headers, data, json_data,isSepehr):
    """Generate a unique Redis cache key based on request parameters."""
    if (isSepehr=='0'):
        request_string = json.dumps({
            'method': method,
            'url': url,
            'params': params,
            'cookies': cookies,
            'headers': headers,
            'data': data,
            'json': json_data,
        }, sort_keys=True)
        return "request_cache:" + hashlib.md5(request_string.encode()).hexdigest()
    if (isSepehr=='1'):
        request_string = json.dumps({
            'method': method,
            'url': url,
            'cookies': cookies,
            'headers': headers,
            'data': data,
            'json': json_data,
        }, sort_keys=True)
        return "request_cache:" + hashlib.md5(request_string.encode()).hexdigest()



def fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port):
    """Fetch response from server and cache it with priorityTimestamp."""
    response = requests.get(full_url, params=serverparams)
    if response.status_code == 200:
        print(
            f"Sent request to {full_url} with priority {priorityTimestamp}, Response: {response.status_code}, port=== {selected_port}")

        # Store response with priorityTimestamp in Redis as a JSON object
        cache_data = {
            "response": response.text,
            "priorityTimestamp": priorityTimestamp
        }
        redis_client.setex(cache_key, 3600, json.dumps(cache_data))  # Cache for 1 hour
        return response.text
    else:
        return []  # Return empty list on failure, per original code


def executeRequest(method, url,
                   params=None, cookies=None,
                   headers=None, data=None,
                   json_data=None,
                   verify=False,
                   priorityTimestamp=1,
                   use_cache='true',
                   forceGet=0,
                   isSepehr='0'):

    if str(use_cache).lower()=='false':
        use_cache=0
    if str(use_cache).lower()=='true':
        use_cache=1


    """Execute a request with caching, priorityTimestamp, and forceGet logic."""
    cache_key = get_cache_key(method, url, params, cookies, headers, data, json_data,isSepehr)

    # Check Redis for cached response
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"Cache hit for {url} )")


    # If this priorityTimestamp doesn't have a server assigned, pick the next one in round-robin
    if priorityTimestamp not in timestamp_server_map:
        timestamp_server_map[priorityTimestamp] = next(server_cycle)

    selected_server = timestamp_server_map[priorityTimestamp]


    # ---------------
    # for priorityTimestamp==1: (to round robin serve)
    #--------------
    if (priorityTimestamp == 1 or priorityTimestamp == '1'):
        selected_server= next(server_cycle)
    # -----------------







    # Select a port from the server's round-robin port cycle
    selected_port = next(server_port_cycles[selected_server])

    # Construct the request URL
    full_url = f"http://{selected_server}:{selected_port}/remoteRequest"

    # Prepare the request parameters
    serverparams = {
        'url': url,
        'params': json.dumps(params) if params is not None else '{}',
        'cookies': json.dumps(cookies) if cookies is not None else '{}',
        'headers': json.dumps(headers) if headers is not None else '{}',
        'method': method,
        'data': json.dumps(data) if data is not None else '{}',
        'json': json.dumps(json_data) if json_data is not None else '{}',
        'priorityTimestamp': priorityTimestamp,
    }
    print(f'Timestamp ======= {priorityTimestamp}')
    # Handle forceGet logic
    if forceGet==1:
        print(f"ForceGet=True: Skipping cache, fetching new response with priority {priorityTimestamp}")
        return fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port)


    # print(f'Redis timestamp === {}')
    if use_cache==1 and cached_data:
        print('caching and haveData...')
        # Use cached response if use_cache=True and cache exists
        cache_data = json.loads(cached_data)
        cached_response = cache_data["response"]
        cached_priority = cache_data["priorityTimestamp"]
        print(f"Cache hit for {url} with priority {cached_priority}")
        return cached_response
    elif use_cache==0 and cached_data:
        print('not caching and checkTimestamp...')
        # When use_cache=False, check priorityTimestamp
        cache_data = json.loads(cached_data)
        cached_priority = cache_data["priorityTimestamp"]
        print(f' eauality ;::::: {cached_priority}  !!!!  {priorityTimestamp}')

        time_difference_seconds = float(priorityTimestamp) - float(cached_priority)

        if time_difference_seconds>5*60:   # 20 second for caching ....

            print(
                f"Skipping cache with older priority {cached_priority}, fetching new response with {priorityTimestamp}---Timeee== {time_difference_seconds}")
            return fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port)
        else:
            print(f"Using cached response with priority {cached_priority} (newer or equal to {priorityTimestamp})")
            return cache_data["response"]
    else:
        print('not data...')
        # No cache exists or forceGet=False with no cache, fetch new response
        return fetch_and_cache_response(full_url, serverparams, cache_key, priorityTimestamp, selected_port)

#
# # Example usage:
# if __name__ == "__main__":
#     response = executeRequest(
#         method="GET",
#         url="https://example.com",
#         priorityTimestamp=1677655000,
#         use_cache=True,
#         forceGet=False
#     )
#     print(response)