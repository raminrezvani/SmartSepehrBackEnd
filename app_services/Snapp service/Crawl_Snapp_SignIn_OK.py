import os
os.system("title Crawl Snapp SignIn OK")
import os
import json
import requests
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
# from insert_influx import Influxdb

from app_crawl.hotel.Client_Dispatch_requests import executeRequest
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# influx = Influxdb()
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=100)  # Adjust the max_workers based on your needs
executor_room = ThreadPoolExecutor(max_workers=100)  # Adjust the max_workers based on your needs

token='ee14f8316cb5ca88776ed7ad50b109d6e25f56722e6dbefdf6e35929d847bcd7c5f7e06c80f717c6dd8cb040bc38fcebc12f'
# Function to get hotel data
def fetch_hotel_data(city_id, date_from, date_to, page):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://business.snapptrip.com',
        'Referer': 'https://business.snapptrip.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-auth-id':  token,  # Replace with actual auth ID
    }
    params = {
        'date_from': date_from,
        'date_to': date_to,
        'orderBy': 'selling',
        'page': str(page),
        'city_id': city_id,
    }
    tries=10
    while True:
        try:
            # response = requests.get('https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params, headers=headers)

            response = executeRequest(method='get',url='https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params,
                                    headers=headers,
                                      use_cache=0 #new retrieval
                                      )


            # response = response.json()
            response = json.loads(response)


            # influx.capture_logs(1, 'Snapp')
            return json.loads(response['text'])
        except:
            print(f'Retrying page {page}...')
            tries=tries-1
            if (tries==0):
                return ''
            # time.sleep(2)

# Function to get room data for a specific hotel
def fetch_room_data(hotelID, date_from, date_to,priorityTimestamp,use_cache):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://business.snapptrip.com',
        'Referer': 'https://business.snapptrip.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-auth-id':token
    }
    params = {
        'date_from': date_from,
        'date_to': date_to,
        'hotel_id': hotelID,
        'page': '1',
    }
    force=0
    while True:
        try:
            # response = requests.get('https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params, headers=headers)
            response = executeRequest(method='get',url='https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params,
                                    headers=headers,
                                    priorityTimestamp=priorityTimestamp,
                                      use_cache=use_cache,
                                      forceGet=force)
            # response=response.json()
            response = json.loads(response)


            # influx.capture_logs(1, 'Snapp')
            return json.loads(response['text'])
        except:
            if (force==1):
                return {}

            print(f'Retrying room data for hotel {hotelID}...')
            force=1
            # time.sleep(2)

cityIDs={
    'KIH':'6918',
    'THR':'6433',
    'IFN':'6326',
    'MHD':'6497',
    'TBZ':'6220',
    'SYZ':'6640',
    'GSM':'6931',
    'AZD':'6969',
    'AWZ':'6541',
    'BND':'6926',
    'KER':'6713',
    'KSH':'6745',
    'RAS':'6814',
    'SRY':'6870',
    'ZBR':'6604',


    # =========
    'ABD':'6549',
    'BUZ':'6390',
    'GBT':'6782',
    'OMH':'6264',
    'ADU':'6288',
    'HDM':'6956',
    'RZR':'6857',
    'KHD':'6839',
    'NSH':'6865',
    #===========






}

# Flask endpoint to get room data
@app.route('/SnappTrip_Hotelrooms', methods=['GET'])
def get_hotel_rooms():
    city_id = request.args.get('city_id')
    target=request.args.get('target')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    isAnalysis = request.args.get('isAnalysis')
    hotelstarAnalysis=request.args.get('hotelstarAnalysis')
    hotelstarAnalysis=json.loads(hotelstarAnalysis)
    priorityTimestamp = request.args.get('priorityTimestamp')
    use_cache=request.args.get('use_cache')


    lst_hotels = []

    #--- read hotels from file hotel_info
    with open(f'Snapp_Hotels/Snapp_Hotels_info_{target}.json', 'r') as f:
        a = f.read()
        hotel_data_results = json.loads(a)

    # lst_hotl=
    # for httt in hotel_data_results:
    #     if ()

    # ======== Check for hotel names or star ratings
    if isAnalysis!='0':
        # Create a set of all hotel names for faster lookup
        all_hotel_names = {hotel['hotel_name'] for hotel in hotel_data_results}
        selected_hotels = set()  # Using set to avoid duplicates

        # Check Redis for hotel name mappings
        for hotel_star in hotelstarAnalysis:
            redis_key = f"asli_hotel:{hotel_star}"
            redis_data = redis_client.get(redis_key)
            if redis_data:
                mapped_hotels = json.loads(redis_data)
                # Add hotels that exist in our current hotels list
                selected_hotels.update(hotel for hotel in mapped_hotels if hotel in all_hotel_names)

        if selected_hotels:
            # If we found mapped hotels, filter the hotels list
            hotel_data_results = [hotel for hotel in hotel_data_results if hotel['hotel_name'] in selected_hotels]
        else:
            # Fallback to original star rating and name check
            hotel_data_results = [hotel for hotel in hotel_data_results
                      if (str(hotel['hotel_star']) in hotelstarAnalysis)
                      or (hotel['hotel_name'] in hotelstarAnalysis)]

        print(f'Snapp Analysis')
    else:
        print(f'Snapp RASII')

    # ============

    # # #---------- Check 5-Star of hotel
    # if (isAnalysis=='1'):
    #     hotel_data_results=[htl for htl in hotel_data_results if str(htl['hotel_star']) in hotelstarAnalysis]
    #     print('Snapp Analysis')
    # else:
    #     print('Snapp RASII')
    # # #------------------------



    # Step 2: Fetch room data in parallel
    room_futures = {executor_room.submit(fetch_room_data, htl['hotel_id'], date_from, date_to,priorityTimestamp,use_cache): htl for htl in
                    hotel_data_results}

    for future in as_completed(room_futures):
        htl = room_futures[future]
        try:
            json_data_room = future.result()
            if 'data' in json_data_room and json_data_room['data']:
                rooms_data = json_data_room['data'][0].get('rooms', [])

                #---
                if 'ساسان' in htl['hotel_name']:
                    print('hotel sasan!')
                #----------

                hotel = {
                    'hotel_name': htl['hotel_name'],
                    'hotel_star': htl['hotel_star'],
                    'min_price': '',
                    'provider': 'Snapp',
                    'rooms': [
                        {
                            'name': rom['title'],
                            'price': rom['prices']['local_price_off'],
                            'capacity': rom['adults'],
                            'provider': 'Snapp',
                        }
                        for rom in rooms_data if rom.get('available_rooms', 0) > 0
                    ]
                }
                lst_hotels.append(hotel)
        except Exception as e:
            print(f"Error fetching room data for {htl['id']}: {e}")

    return jsonify(lst_hotels)

#
# def get_hotel_rooms_old():
#     city_id = request.args.get('city_id')
#     date_from = request.args.get('date_from')
#     date_to = request.args.get('date_to')
#     lst_hotels = []
#
#     futures = []
#     for i in range(1, 10):  # Assuming 4 pages of hotels
#         futures.append(executor.submit(fetch_hotel_data, city_id, date_from, date_to, i))
#
#     lst_unique_hotels=[]
#     for future in as_completed(futures):
#         json_data = future.result()
#         for htl in json_data['data']:
#             hotelName = htl['title']
#
#
#
#
#             hotelID = htl['id']
#             hotel = {
#                 'hotel_name': hotelName,
#                 'hotel_star': htl['stars'],
#                 'min_price': '',
#                 'provider': 'Snapp',
#                 'rooms': []
#             }
#             # Fetch room data in a new thread
#             room_data_future = executor_room.submit(fetch_room_data, hotelID, date_from, date_to)
#
#             json_data_room = room_data_future.result()
#             rooms = json_data_room['data'][0]['rooms']
#             for rom in rooms:
#                 available_rooms=rom['available_rooms']
#                 if (rom['available_rooms']==0):
#                     continue
#
#                 room = {
#                     'name': rom['title'],
#                     'price': rom['prices']['local_price_off'],
#                     'capacity':rom['adults'],
#                     'provider': 'Snapp',
#                 }
#                 hotel['rooms'].append(room)
#             lst_hotels.append(hotel)
#
#     return jsonify(lst_hotels)




#---------------------


def get_hotels_info_writeJson():
    # lst_targets = list(Dic_mapping_destination.keys())
    start_date = datetime.today() + timedelta(days=4)
    start_date = start_date.strftime("%Y-%m-%d")

    end_date = datetime.today() + timedelta(days=7)
    end_date = end_date.strftime("%Y-%m-%d")


    for target in list(cityIDs.keys()):

        if os.path.exists(f'Snapp_Hotels/Snapp_Hotels_info_{target}.json'):
            ''
        else:


            city_id=cityIDs[target]
            # Step 1: Fetch hotel data in parallel
            futures = {executor.submit(fetch_hotel_data, city_id, start_date, end_date, i): i for i in range(1, 10)}
            hotel_data_results = []

            for future in as_completed(futures):
                json_data = future.result()
                if 'data' in json_data:
                    hotel_data_results.extend(json_data['data'])  # Collect hotel data first

            lst_hotels=[]
            lst_unique_hotels=[]
            #--- parse each hotel
            for htl in hotel_data_results:
                hotel_info={}
                hotel_info['hotel_id']=htl['id']
                hotel_info['hotel_name']=htl['title']

                # --- redundant hotelName
                if (hotel_info['hotel_name'] in lst_unique_hotels):
                    continue
                lst_unique_hotels.append(hotel_info['hotel_name'])
                # ------


                try:
                    hotel_info['hotel_star'] = htl['stars']
                except:
                    hotel_info['hotel_star']=3
                    print('error')

                lst_hotels.append(hotel_info)
            #------
            if not os.path.exists('Snapp_Hotels'):
                os.makedirs('Snapp_Hotels')  # Creates the folder

            json.dump(lst_hotels, open(f'Snapp_Hotels/Snapp_Hotels_info_{target}.json', 'w'))
            print(f'Snapp_Hotels/Snapp_Hotels_info_{target}.json  is created!')
    #=------------

#--- for first time ----
get_hotels_info_writeJson()
#=================




#_-----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, threaded=False)

