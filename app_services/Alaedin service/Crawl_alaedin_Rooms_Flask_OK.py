# cd C:\Users\Administrator\PycharmProjects\web\vn\Scripts
# activate
# cd C:\Users\Administrator\Desktop\SepehrSmart_services
# python Crawl_alaedin_Rooms_Flask_OK.py

import os
import json
import requests
import jdatetime
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import jdatetime
from app_crawl.hotel.Client_Dispatch_requests import executeRequest

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from insert_influx import Influxdb
# influx = Influxdb()


# Set a title for the CMD window
os.system("title Crawl Alaedin Rooms Flask")

# Function to get the Shamsi date seven days from now
def get_shamsi_date():
    d1 = datetime.now() + timedelta(days=7)
    shamsi_date = jdatetime.datetime.fromgregorian(datetime=d1)
    return str(shamsi_date.date()).replace('-', '')

# Function to load cookies and headers from a JSON file
def load_cookies_and_headers(output_file):
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            data = json.load(f)
            return data.get("request_headers", {}), data.get("cookies_dict", {})
    return None, None

# Function to save cookies and headers to a JSON file
def save_cookies_and_headers(output_file, headers, cookies):
    with open(output_file, 'w') as f:
        json.dump({"request_headers": headers, "cookies_dict": cookies}, f, indent=4)

def sign_IN(driver):
    while True:
        try:
            driver.get('https://www.alaedin.travel/account/login')
            driver.find_element(By.XPATH, '//input[@name="userName"]').clear()
            driver.find_element(By.XPATH, '//input[@name="userName"]').send_keys('0920262961')
            driver.find_element(By.XPATH, '//input[@name="password"]').clear()
            driver.find_element(By.XPATH, '//input[@name="password"]').send_keys('MST1231020')
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            print('SignIn Successful!')
            break
        except:
            print('Error in SignIn --- retrying ...')

# Function to get headers and cookies from Alaedin website
def get_alaedin_cookies_headers(url, output_file):
    options = webdriver.ChromeOptions()
    with webdriver.Chrome(seleniumwire_options={}, options=options) as driver:
        # Sign in
        sign_IN(driver)
        time.sleep(5)
        driver.get(url)
        time.sleep(3)
        while(True):
            try:
                # Filter for the specific API request
                for request in driver.requests:
                    if request.url.startswith("https://www.alaedin.travel/GetHotels/GetRoomPrice") and request.response:
                        request_headers = dict(request.headers)
                        request_cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                        save_cookies_and_headers(output_file, request_headers, request_cookies)
                        return request_headers, request_cookies
            except:
                print('selenium-wire error')
                time.sleep(2)
    return {}, {}

# Setup Flask app
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=100)  # Use multiple threads for concurrency

# Endpoint to get room data
@app.route('/Alaedin_rooms', methods=['GET'])
def get_rooms():
    hotelCod = request.args.get('hotelCod')
    start_date = request.args.get('start_date')
    stay = request.args.get('stay')
    priorityTimestamp = request.args.get('priorityTimestamp')
    use_cache=request.args.get('use_cache')


    # Run request in a separate thread
    future = executor.submit(fetch_room_data, hotelCod, start_date, stay,priorityTimestamp,use_cache)
    result = future.result()  # Wait for the thread to finish and get the result

    return jsonify(result)
import time
# Function to handle fetching room data
def fetch_room_data(hotelCod, start_date, stay,priorityTimestamp,use_cache):

    while(True):
        try:

            year, month, day = map(int, start_date.split("-"))
            jalali_date = jdatetime.date(year, month, day)
            endDate = jalali_date + jdatetime.timedelta(days=int(stay))

            data = {
                'hotelCod': f'{hotelCod}',
                'stDate': f'{start_date}',
                'endDate': f'{endDate}',
                'reslong': f'{stay}',
                'reslongInt': f'{stay}',
            }


            # response = requests.post(
            #     f'https://www.alaedin.travel/GetHotels/GetRoomPrice?'
            #     f'hotelCod={hotelCod}'
            #     f'&stDate={start_date}'
            #     f'&reslong={stay}'
            #     f'&searchId=',
            #     cookies=cookies_dict,
            #     headers=request_headers,
            #     data=data
            # )


            response = executeRequest(method='post',
                url=f'https://www.alaedin.travel/GetHotels/GetRoomPrice?'
                f'hotelCod={hotelCod}'
                f'&stDate={start_date}'
                f'&reslong={stay}'
                f'&searchId=',
                cookies=cookies_dict,
                headers=request_headers,
                data=data,
                priorityTimestamp=priorityTimestamp,
                use_cache=use_cache

            )
            # response=response.json()
            response = json.loads(response)



            # influx.capture_logs(1, 'Alaedin')

            break
        except:
            print('Error on fetch_room_data ...')
            time.sleep(2)
            continue

    return response

if __name__ == '__main__':
    shamsi_date_api = get_shamsi_date()
    output_file = "Alaedin_cookies.json"

    # Load existing cookies and headers or retrieve them from Alaedin if not available
    request_headers, cookies_dict = load_cookies_and_headers(output_file)
    if not request_headers or not cookies_dict:
        url = f'https://www.alaedin.travel/hotels/kish/arya/{shamsi_date_api}/3'
        request_headers, cookies_dict = get_alaedin_cookies_headers(url, output_file)

    # Run Flask app with threading enabled
    app.run(host='0.0.0.0', port=5003, threaded=True)


#============ OLD Code==========
# import os
# os.system("title  Crawl Alaedin Rooms Flask")
#
# import os
# import json
# import requests
# import jdatetime
# from datetime import datetime, timedelta
# from flask import Flask, request, jsonify
# # from concurrent.futures import ThreadPoolExecutor
# from seleniumwire import webdriver
# from selenium.webdriver.common.by import By
# # Function to get the Shamsi date seven days from now
# def get_shamsi_date():
#     d1 = datetime.now() + timedelta(days=7)
#     shamsi_date = jdatetime.datetime.fromgregorian(datetime=d1)
#     return str(shamsi_date.date()).replace('-', '')
#
# # Function to load cookies and headers from a JSON file
# def load_cookies_and_headers(output_file):
#     if os.path.exists(output_file):
#         with open(output_file, 'r') as f:
#             data = json.load(f)
#             return data.get("request_headers", {}), data.get("cookies_dict", {})
#     return None, None
#
# # Function to save cookies and headers to a JSON file
# def save_cookies_and_headers(output_file, headers, cookies):
#     with open(output_file, 'w') as f:
#         json.dump({"request_headers": headers, "cookies_dict": cookies}, f, indent=4)
#
# def sign_IN(driver):
#     # driver.set_page_load_timeout(20)
#     while(True):
#         try:
#             driver.get('https://www.alaedin.travel/account/login')
#             driver.find_element(By.XPATH, '//input[@name="userName"]').clear()
#             driver.find_element(By.XPATH, '//input[@name="userName"]').send_keys('0920262961')
#
#             driver.find_element(By.XPATH, '//input[@name="password"]').clear()
#             driver.find_element(By.XPATH, '//input[@name="password"]').send_keys('MST1231020')
#
#             driver.find_element(By.XPATH, '//button[@type="submit"]').click()
#             print('SingIn Successfull!')
#             break
#         except:
#             print('error in SignIN --- retry ...')
#
#
# # Function to get headers and cookies from Alaedin website
# def get_alaedin_cookies_headers(url, output_file):
#     options = webdriver.ChromeOptions()
#     with webdriver.Chrome(seleniumwire_options={}, options=options) as driver:
#         #-- sign in
#         sign_IN(driver)
#
#         driver.get(url)
#
#         # Filter for the specific API request
#         for request in driver.requests:
#             if request.url.startswith("https://www.alaedin.travel/GetHotels/GetRoomPrice") and request.response:
#                 request_headers = dict(request.headers)
#                 request_cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
#                 save_cookies_and_headers(output_file, request_headers, request_cookies)
#                 return request_headers, request_cookies
#     return {}, {}
#
# # Setup Flask app
# app = Flask(__name__)
# # executor = ThreadPoolExecutor(max_workers=1)
#
# # Endpoint to get room data
# @app.route('/Alaedin_rooms', methods=['GET'])
# def get_rooms():
#     hotelCod = request.args.get('hotelCod')
#     start_date = request.args.get('start_date')
#     stay = request.args.get('stay')
#
#     response = requests.get(
#         f'https://www.alaedin.travel/GetHotels/GetRoomPrice?'
#         f'hotelCod={hotelCod}'
#         f'&stDate={start_date}'
#         f'&reslong={stay}'
#         f'&searchId=',
#         cookies=cookies_dict,
#         headers=request_headers,
#     )
#
#     return jsonify(response.json())
#
# if __name__ == '__main__':
#     shamsi_date_api = get_shamsi_date()
#     output_file = "Alaedin_cookies.json"
#
#     # Load existing cookies and headers or retrieve them from Alaedin if not available
#     request_headers, cookies_dict = load_cookies_and_headers(output_file)
#     if not request_headers or not cookies_dict:
#         url = f'https://www.alaedin.travel/hotels/kish/arya/{shamsi_date_api}/3'
#         request_headers, cookies_dict = get_alaedin_cookies_headers(url, output_file)
#
#     app.run(host='0.0.0.0', port=5003,threaded=False)
