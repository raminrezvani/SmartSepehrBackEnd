import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from threading import Thread

import requests
from requests import request
from app_crawl.helpers import convert_to_tooman
import urllib3
from app_crawl.hotel.Client_Dispatch_requests import executeRequest

from app_crawl.insert_influx import Influxdb
import traceback
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hotelIDs = {
    'THR': '400',
    'MHD': '401',
    'IFN': '399',
    'SYZ': '412',
    'KIH': '402',
    'GSM': '448',
    'AZD': '421',
    'TBZ': '439',

    'AWZ': '433',
    'BND': '4792',
    'KER': '419',
    'KSH': '427',
    'RAS': '442',
    'SRY': '446',
    'ZBR': '411',
    'ABD': '428',
    'BUZ': '437',
    'GBT': '426',
    'OMH': '432',
    'ADU': '409',
    'HDM': '415',
    'RZR': '441',
    'KHD': '440',
    'NSH': '424',

}


class Deltaban:
    isAnalysis=False
    def __init__(self, target, start_date, end_date, adults,isAnalysiss,hotelstarAnalysis=[],priorityTimestamp=1,
                 use_cache=True):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.isAnalysis=isAnalysiss[0] if isAnalysiss is tuple else isAnalysiss ,
        self.isAnalysis = self.isAnalysis[0] if isinstance(self.isAnalysis, tuple) else self.isAnalysis
        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp=priorityTimestamp
        self.use_cache=use_cache
        self.influx = Influxdb()

        # self.executor = ThreadPoolExecutor(max_workers=50)
        self.request_header = {
            'Content-Type': 'application/json',
            "authorization": ""
        }
        self.login = {
            "username": "mojalal",  # default => deltaban_guest
            "password": "@MST8451030yf"  # default => guest
        }
        self.token_file = "deltaban_access_token.json"  # File to store the access token
        self.get_authorization()



    def get_authorization(self):
        """
        Retrieve the access token from the file if it exists.
        If the token is not available or invalid, request a new token
        and save it to the file.
        """
        # Check if token file exists and load it
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as file:
                data = json.load(file)
                access_token = data.get("access_token")
                if access_token:  # If a valid token is found
                    self.request_header['authorization'] = access_token
                    return access_token

        # Token not found or invalid, request a new one
        url = "https://api.3click.com/auth/Login"
        headers = {
            'provider-code': 'deltaban',
            'Content-Type': 'application/json',
        }

        # response = requests.post(url, headers=headers, data=json.dumps(self.login), verify=False)
        response = executeRequest(method='post',
                                  url=url,
                                  headers=headers,
                                  data=json.dumps(self.login),
                                  verify=False,
                                  priorityTimestamp=self.priorityTimestamp,
                                  use_cache=self.use_cache)
        # response=response.json()
        response=json.loads(response)




        self.influx.capture_logs(1, 'deltaban')

        if response['status_code'] != 200:
            print(f"Deltaban Failed to authenticate: {response['status_code']}, {response['text']}")
            return ''


        # Parse the new access token
        # data = response.json()
        data = json.loads(response['text'])
        access_token = f"JWT {data['access_token']}"

        # Save the access token to a file
        with open(self.token_file, "w") as file:
            json.dump({"access_token": access_token}, file)

        # Update the request header
        self.request_header['authorization'] = access_token
        return access_token

    #
    # def get_authorization_OLD(self):
    #     url = "https://api.3click.com/auth/Login"
    #     headers = {
    #         'provider-code': 'deltaban',
    #         'Content-Type': 'application/json',
    #     }
    #     tryed=0
    #     response = request("POST", url, headers=headers, data=json.dumps(self.login), verify=False)
    #     if response.status_code != 200:
    #         # if (tryed==3):
    #         #     return ''
    #         self.get_authorization_OLD()
    #
    #     data = json.loads(response.text)
    #
    #     access_token = f"JWT {data['access_token']}"
    #
    #     self.request_header['authorization'] = access_token
    #     return access_token

    def get_token(self):

        req_url = f"https://api.3click.com/api/hotel/core/v1/Hotels/cities/{hotelIDs[self.target]}/available"

        req_body = json.dumps({
            "checkIn": self.start_date,
            "checkOut": self.end_date,
            "roomPassengers": [
                {
                    "childrenAges": [],
                    "adultsCount": self.adults
                }
            ]
        })

        req = request("POST", req_url, headers=self.request_header, data=req_body)
        # self.influx.capture_logs(1, 'deltaban')

        data = json.loads(req.text)

        return data['searchToken']

    def get_room_token(self, hotel_id):
        req_url = f"https://api.3click.com/api/hotel/core/v1/Hotels/{hotel_id}/availablepackages"

        req_body = {
            "checkIn": self.start_date,
            "checkOut": self.end_date,
            "isTourDynamic": False,
            "roomPassengers": [
                {
                    "childrenAges": [],
                    "adultsCount": self.adults
                }
            ],
            "searchToken": ""
        }

        req = request("POST", req_url, json=req_body, headers=self.request_header)
        self.influx.capture_logs(1, 'deltaban')

        return json.loads(req.text)['searchToken']

    def get_hotels(self):
        token = self.get_token()

        req_url = f"https://api.3click.com/api/hotel/core/v1/Hotels/{token}/Search"

        counter = 0
        result = []
        while counter < 22:



            # req = request("GET", req_url, headers=self.request_header)
            req = executeRequest(method="GET",url= req_url,
                                 headers=self.request_header,priorityTimestamp=self.priorityTimestamp,
                                 use_cache=self.use_cache)
            # req=req.json()
            req = json.loads(req)

            self.influx.capture_logs(1,'deltaban')

            data = json.loads(req['text'])

            counter += 1
            # ---
            result.extend(data['items'])
            # ---
            if data['isFinish']:
                break
        return result

    def fetch_data(self,req_url, request_header):
        try:
            # req = request("GET", req_url, headers=request_header)
            req = executeRequest(method="GET", url=req_url,
                                 headers=request_header,priorityTimestamp=self.priorityTimestamp,
                                 use_cache=self.use_cache)
            # req=req.json()
            req = json.loads(req)


            self.influx.capture_logs(1, 'deltaban')

            data = json.loads(req['text'])

            rooms = [
                {
                    "price": convert_to_tooman(room['packagePrice']),
                    "name": room['roomTypes'][0]['name'],
                    "provider": "deltaban",
                }
                for room in data['items']
            ]

            if data['isFinish']:
                print('ok shod')
                return rooms, True

            return rooms, False
        except Exception as e:
            print(f"Error occurred: {e}")
            return [], False

    def get_hotels_info_writeJson(self):
        #---------------------
        # save results of hotels into folder
        #--------------
        hotels = self.get_hotels()
        lst_res_hotels=[]
        for htl in hotels:
            htl_info={}
            htl_info['hotelId']=htl['hotelId']
            htl_info['hotel_name']= htl['persianName']
            htl_info['hotel_star']= htl['star']
            htl_info['min_price']=convert_to_tooman(htl['minimumPackagePrice'])
            lst_res_hotels.append(htl_info)


        # ------------ save hotesl into file
        if not os.path.exists('Deltaban_hotels'):
            os.makedirs('Deltaban_hotels')  # Creates the folder

        json.dump(lst_res_hotels, open(f'Deltaban_hotels/Deltaban_hotels_info_{self.target}.json', 'w'))
        # --------------


    def get_result(self):

        # ---- Load hotels info from Json
        with open(f'Deltaban_hotels/Deltaban_hotels_info_{self.target}.json', 'r') as f:
            a = f.read()
            hotels = json.loads(a)
        #---------------------

        result = []

        def room_handler(hotel):
            hotel_id = hotel['hotelId']
            room_token = self.get_room_token(hotel_id)

            req_url = f"https://api.3click.com/api/hotel/core/v1/Hotels/{room_token}/searchpackages?hotelId={hotel_id}"

            counter = 0
            rooms = []

            # #================ NEW CODE ===================
            # rooms = []
            # req_urls = [req_url for i in range(5)]  # Create 20 unique request URLs
            #
            # with ThreadPoolExecutor(max_workers=20) as executor:
            #     futures = [executor.submit(self.fetch_data, req_url, self.request_header) for url in req_urls]
            #
            #     for future in as_completed(futures):
            #         try:
            #             result, is_finish = future.result()
            #             rooms.extend(result)
            #             if is_finish:
            #                 print("Final data fetched.")
            #                 # return rooms
            #         except Exception as e:
            #             print(f"Error occurred: {e}")


            # #=========== OLD ===========================
            # while counter < 2:
            while (True):
                try:
                    while(counter<20):
                        # req = request("GET", req_url, headers=self.request_header)
                        req = executeRequest(method="GET",url= req_url, headers=self.request_header,priorityTimestamp=self.priorityTimestamp,
                                             use_cache=self.use_cache)
                        # req=req.json()
                        req = json.loads(req)


                        # self.influx.capture_logs(1, 'deltaban')
                        data={}
                        try:
                            data = json.loads(req['text'])
                        except:
                            # print(f'req ==== {req}')
                            # counter += 1
                            break
                            # continue


                        counter += 1

                        rooms.extend([{
                            "price": convert_to_tooman(room['packagePrice']),
                            "name": room['roomTypes'][0]['name'],
                            "provider": "deltaban",
                            "capacity":room['roomTypes'][0]['capacity'],

                        } for room in data['items']])
                        if data['totalCount']!=0 :
                            print('ok shod')
                            break
                        # if data['isFinish']:
                        #     print('ok shod')
                        #     break
                    break
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f'Except occured in get_result_deltaban == {str(e)}')
                    print(f"Traceback details:\n{tb}")
                    counter += 1
                    # time.sleep(1)
                    continue
            # #=======================================


            result.append({
                "hotel_name": hotel['hotel_name'],
                "hotel_star": hotel['hotel_star'],
                "min_price": hotel['min_price'],
                "rooms": rooms,
                "provider": "deltaban"
            })


        #======== Check for hotel names or star ratings
        if self.isAnalysis:
            # Create a set of all hotel names for faster lookup
            all_hotel_names = {hotel['hotel_name'] for hotel in hotels}
            selected_hotels = set()  # Using set to avoid duplicates

            # Check Redis for hotel name mappings
            for hotel_star in self.hotelstarAnalysis:
                redis_key = f"asli_hotel:{hotel_star}"
                redis_data = redis_client.get(redis_key)
                if redis_data:
                    mapped_hotels = json.loads(redis_data)
                    # Add hotels that exist in our current hotels list
                    selected_hotels.update(hotel for hotel in mapped_hotels if hotel in all_hotel_names)

            if selected_hotels:
                # If we found mapped hotels, filter the hotels list
                hotels = [hotel for hotel in hotels if hotel['hotel_name'] in selected_hotels]
            else:
                # Fallback to original star rating and name check
                hotels = [hotel for hotel in hotels
                         if (str(hotel['hotel_star']) in self.hotelstarAnalysis)
                         or (hotel['hotel_name'] in self.hotelstarAnalysis)]

            print(f'Deltaban Analysis')
        else:
            print(f'Deltaban RASII')

        #============


        #==== More efficient ====

        # Determine optimal thread count: min(tasks, max_threads)
        optimal_threads = min(len(hotels), 100) if len(hotels)!=0 else 1  # Set a reasonable max limit (e.g., 10)

        with ThreadPoolExecutor(max_workers=optimal_threads) as executor:


            # Submit tasks and collect futures
            futures = {executor.submit(room_handler, hotel): hotel for hotel in hotels}

            timeout_seconds = 20 # Set your desired timeout


            # Wait for tasks to complete and handle results
            for future in as_completed(futures, timeout=timeout_seconds):
                # hotel = futures[future]
                try:
                    future.result()  # Get result of the task
                    # print(result)
                except Exception as e:
                    print('Errrrrorr')
                    print(f"Error processing : {e}")

        # print("All tasks are completed.")

        #=======
        # with ThreadPoolExecutor(max_workers=100) as executor:
        #     executor.map(room_handler, hotels)

        return result







# Function to delete cookies.json every 3 hours
def delete_cookies_periodically():
    while True:
        # Wait for 3 hours (3 hours * 60 minutes * 60 seconds)
        time.sleep(20 * 60 * 60)
        # Check if cookies.json exists and delete it
        if os.path.exists('deltaban_access_token.json'):
            os.remove('deltaban_access_token.json')
            print("Deleted deltaban_access_token.json")
            #-- create again
            # create_cookie_with_selenium()
            # manually mishavad dorost konad!


# Start the background thread for cookie deletion
cookie_deletion_thread = Thread(target=delete_cookies_periodically)
cookie_deletion_thread.daemon = True  # Daemonize thread to exit when the main program exits
cookie_deletion_thread.start()





# === for first time = (create hotel info )
from datetime import datetime,timedelta
# with open(f'Booking_hotel_info_{self.target}.json','r') as f:
lst_targets1=list(hotelIDs.keys())
start_date1 = datetime.today() + timedelta(days=4)
start_date1 = start_date1.strftime("%Y-%m-%d")

end_date1 = datetime.today() + timedelta(days=7)
end_date1 = end_date1.strftime("%Y-%m-%d")

isAnalysiss = False
adults = '2'
import concurrent.futures


for tg in lst_targets1:
    if os.path.exists(f'Deltaban_hotels/Deltaban_hotels_info_{tg}.json'):
        ''
    else:

        ins = Deltaban(tg, start_date1, end_date1, adults, isAnalysiss, hotelstarAnalysis=[])
        ins.get_hotels_info_writeJson()
        print(f'Deltaban_hotels/Deltaban_hotels_info_{tg}.json  is created!')

# =================





# from time import perf_counter
#
# start = perf_counter()
#
# deltaban = Deltaban("KIH", "2023-02-10", "2023-02-14", 2)
# print("--------------------------------")
# print(deltaban.get_result())
#
# end = perf_counter()
#
# print("--------------------------------")
# print(f"end with ==> {round(end - start, 2)} seconds")
