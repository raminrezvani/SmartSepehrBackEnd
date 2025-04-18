import os

os.system("title Distribute Requests")
from flask import Flask, jsonify, request
import json
from lxml import etree
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
import requests
import queue
import threading
import time
from insert_influx import Influxdb
from concurrent.futures import Future
influx = Influxdb()

app = Flask(__name__)

task_queue = queue.PriorityQueue()  # Priority queue for tasks
executor = ThreadPoolExecutor(max_workers=10000)  # 10 worker threads
condition = threading.Condition()


def process_requests():
    """Worker function that retrieves and executes tasks from the queue"""
    while True:
        with condition:
            while task_queue.empty():
                condition.wait()  # Wait until there is a task in the queue

            priority, count, task = task_queue.get()  # Unpack three values

        # print(f"Executing Task {task.task_id} (Priority: {priority})")
        future = executor.submit(task.execute)  # Assign task to a worker thread

        try:
            result = future.result()
            if result:
                task.future.set_result(result)  # Store response in future
        except:
            # task.future.set_exception(ValueError("No valid response received"))
            # Create an empty response object
            empty_response = requests.Response()

            # Set attributes to simulate an empty response
            empty_response._content = b''  # Empty content
            empty_response.status_code = 204  # No Content status code
            empty_response.headers = {}  # Empty headers

            # self.future.set_exception(ValueError("No valid response received"))
            task.future.set_result(empty_response)


        # print(f"Completed Task {task.task_id}: {result}")




# executor = ThreadPoolExecutor(max_workers=10000)
# executor = ThreadPoolExecutor(max_workers=1)
# # response = requests.get('https://www.eghamat24.com/property-rooms/list-view', params=params, cookies=cookies, headers=headers)
class ExeRequest:
    def __init__(self, method, url, params=None, cookies=None, headers=None, data=None, json=None):
        self.url = url
        self.params = params
        self.cookies = cookies
        self.headers = headers
        self.method = method.lower()  # Convert to lowercase for consistency
        self.data = data
        self.json = json
        self.future = Future()  # Future object to store result

    def execute(self):
        numTries=2
        response = None
        while(True):
            try:
                if self.method == "get":
                    response = requests.get(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
                                            data=self.data, json=self.json)
                elif self.method == "post":
                    response = requests.post(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
                                             data=self.data, json=self.json)
                else:
                    response = None
                    # raise ValueError(f"Unsupported HTTP method: {self.method}")
                break
            except:
                numTries=numTries-1
                if (numTries == 0):
                    response = None
                    break
                continue


        # If response is None (e.g., unsupported method), set an exception
        if response is None:

            # Create an empty response object
            empty_response = requests.Response()

            # Set attributes to simulate an empty response
            empty_response._content = b''  # Empty content
            empty_response.status_code = 204  # No Content status code
            empty_response.headers = {}  # Empty headers

            # self.future.set_exception(ValueError("No valid response received"))
            self.future.set_result(empty_response)

        else:
            # Otherwise, set the result in the Future
            self.future.set_result(response)

        # self.future.set_result(response)  # Store result in Future
        # return response  # Return the response object


import itertools

task_counter = itertools.count()  # Unique counter for tasks
@app.route('/remoteRequest', methods=['GET'])
def remoteRequest():
    url = request.args.get('url','')
    params = json.loads(request.args.get('params', '{}'))  # Parse params as JSON
    cookies = json.loads(request.args.get('cookies', '{}'))  # Parse cookies as JSON
    headers = json.loads(request.args.get('headers', '{}'))  # Parse headers as JSON
    method = request.args.get('method','GET').lower()        # Convert to lowercase for consistency
    data = json.loads(request.args.get('data', '{}')) if method == "post" or method=="POST" else None  # Parse data if POST
    json_data = json.loads(request.args.get('json', '{}')) if method == "post" or method=="POST" else None  # Parse json if POST

    print(f'AJABB =-----  {request.args.get("priorityTimestamp")}')

    priority = float(request.args.get('priorityTimestamp', time.time()))  # Default to current time

    print(f'Get address with priority== {priority}')

    exeRequest = ExeRequest(method, url, params, cookies, headers, data, json_data)
    maxTries=3
    while(True):

        if (maxTries<=0):
            print('FAIIILLEEDDDDD.....')
            return jsonify({
                'status_code': '500',
                'text': [],
                'cookies': []
            })

        with condition:
            count = next(task_counter)  # Get a unique counter value
            task_queue.put((priority, count, exeRequest))  # Store priority, counter, and request

            # task_queue.put((priority, exeRequest))  # Add task with priority
            condition.notify()  # Wake up a worker thread

        print(f"Queued Task ??? with Priority {priority}")



        try:
            # Wait for task execution and return the result
            result = exeRequest.future.result()  # Wait until the task is completed
            # Extract the status code, text, and cookies
            status_code = result.status_code
            text = result.text
            cookies = result.cookies.get_dict()  # Convert cookies to a dictionary for easy access
        except:
            maxTries=maxTries-1
            continue

        # Return the information as JSON
        return jsonify({
            'status_code': status_code,
            'text': text,
            'cookies': cookies
        })
        break




    # future = executor.submit(exeRequest.execute,)
    # # result = future.result()
    # # print(f'Send result == ')
    # # Optionally, you can return a response immediately
    # # return jsonify(result)
    #
    # # Extract the status code, text, and cookies
    # status_code = result.status_code
    # text = result.text
    # cookies = result.cookies.get_dict()  # Convert cookies to a dictionary for easy access
    #
    #
    # # Return the information as JSON
    # return jsonify({
    #     'status_code': status_code,
    #     'text': text,
    #     'cookies': cookies
    # })
    # return result

# Start 10 worker threads
for _ in range(1000):
    threading.Thread(target=process_requests, daemon=True).start()


import sys
if __name__ == '__main__':
    port=int(sys.argv[1]) # Get port from command line
    # app.run(debug=True,host='0.0.0.0',port=6000)
    app.run(host='0.0.0.0',port=port)
