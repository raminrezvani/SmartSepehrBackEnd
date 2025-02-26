import requests
import itertools

# # Define servers and ports
# servers = [
#     # ("45.149.76.168", [6000]),
#     ("mqtt.angizehco.com", [6000, 6001, 6002,6003,6004,6005]),
#     ("45.149.76.168", [6000, 6001, 6002,6003,6004,6005]),
#     ("130.185.77.24", [6000, 6001, 6002,6003,6004,6005]),
#     # ("185.252.31.31", [6000, 6001, 6002,6003,6004,6005])
# ]
#
# # Create an iterator for round-robin selection
# server_iterator = itertools.cycle([(server, port) for server, ports in servers for port in ports])



# Define servers and ports
servers = [
    # ("mqtt.angizehco.com", [6000, 6001, 6002, 6003, 6004, 6005]),
    ("45.149.76.168", [6000, 6001, 6002, 6003, 6004, 6005]),
    # ("130.185.77.24", [6000, 6001, 6002, 6003, 6004, 6005]),
]


# Create a list of server:port combinations for each port
server_port_list = [
    f"{server}:{port}"
    for port in set(port for _, ports in servers for port in ports)
    for server, ports in servers if port in ports
]



from itertools import cycle



# Create a round-robin cycle from the list
server_cycle = cycle(server_port_list)

# Function to get the next item in a round-robin manner
def next_server():
    return next(server_cycle)




import json
# req = requests.post('https://www.booking.ir/fa/v2/signinbymobile/', headers=headers, data=data)
def executeRequest(method, url,
                   params=None, cookies=None,
                   headers=None, data=None,
                   json_data=None,
                   verify=False,
                   priorityTimestamp=1):
    # Select the next server and port in a round-robin fashion

    server, port = next_server().split(':')  # Get next server-port pair

    # server, port = next(server_iterator)
    full_url = f"http://{server}:{port}/remoteRequest"
    # print(f"Executing request to: {full_url}")



    serverparams = {
        'url': url,
        'params': json.dumps(params) if params is not None else '{}',  # Ensure it's a JSON object
        'cookies': json.dumps(cookies) if cookies is not None else '{}',
        'headers': json.dumps(headers) if headers is not None else '{}',
        'method': method,
        'data': json.dumps(data) if data is not None else '{}',
        'json': json.dumps(json_data) if json_data is not None else '{}',
        'priorityTimestamp': priorityTimestamp,
    }


    # round robin for server 45.149.76.168 with ports [6000,6001,6002] and server 130.185.77.24 with ports [6000,6001,6002]
    response = requests.get(full_url, params=serverparams)

    return response # Return the response object


