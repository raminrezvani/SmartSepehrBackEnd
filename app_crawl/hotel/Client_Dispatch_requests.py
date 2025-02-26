import requests
import json
import redis
from itertools import cycle
import hashlib

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# Define servers and ports
servers = [
    ("45.149.76.168", [6000, 6001, 6002,6003,6004,6005]),
    ("130.185.77.24", [6000, 6001, 6002,6003,6004,6005]),
]

# Round-robin cycle for selecting servers
server_cycle = cycle([server for server, _ in servers])

# Dictionary to store which server is assigned to each priorityTimestamp
timestamp_server_map = {}

# Dictionary to store round-robin port selection for each server
server_port_cycles = {
    server: cycle(ports) for server, ports in servers
}


def get_cache_key(method, url, params, cookies, headers, data, json_data):
    """Generate a unique Redis cache key based on request parameters."""
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


def executeRequest(method, url,
                   params=None, cookies=None,
                   headers=None, data=None,
                   json_data=None,
                   verify=False,
                   priorityTimestamp=1):

    cache_key = get_cache_key(method, url, params, cookies, headers, data, json_data)
    # Check Redis for cached response
    cached_response = redis_client.get(cache_key)
    if cached_response:
        print(f"Cache hit for {url} )")
        # return json.loads(cached_response)  # Returning JSON-compatible object
        return cached_response  # Returning JSON-compatible object


    # If this priorityTimestamp doesn't have a server assigned, pick the next one in round-robin
    if priorityTimestamp not in timestamp_server_map:
        timestamp_server_map[priorityTimestamp] = next(server_cycle)

    selected_server = timestamp_server_map[priorityTimestamp]

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

    # Send the request
    response = requests.get(full_url, params=serverparams)



    # # Convert response to JSON format before caching
    # try:
    #     response_json = response.json()  # Ensure response is JSON-parsable
    # except ValueError:
    #     response_json = {"status_code": response['status_code'],
    #                      "text": response['text'],
    #                      'cookies':response['cookies']}  # Fallback in case of non-JSON



    print(f"Sent request to {full_url} with priority {priorityTimestamp}, Response: {response.status_code}, port=== {selected_port}")


    # Cache the response in Redis
    redis_client.setex(cache_key, 3600, response.text)  # Store JSON directly
    # redis_client.setex(cache_key, 3600, json.dumps(response))  # Store JSON directly



    return response.text  # Return the response object
