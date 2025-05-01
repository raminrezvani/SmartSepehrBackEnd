# #--- another approach
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
#
# # Enable logging for performance (CDP)
# options = Options()
# options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
#
# # Initialize WebDriver
# service = Service("chromedriver.exe")  # Replace with the correct path to your ChromeDriver
# driver = webdriver.Chrome(service=service, options=options)
# #
# # # Open a webpage
# # driver.get("https://example.com")
# #
# # # Extract network logs
# # logs = driver.get_log("performance")
# # for log in logs:
# #     print(log)
#
# # Get cookies for the current domain
# cookies = driver.get_cookies()
# for cookie in cookies:
#     print(f"Name: {cookie['name']}, Value: {cookie['value']}")
#
# driver.quit()
#

# cd C:\Users\Administrator\PycharmProjects\web\vn\Scripts
# activate
# cd C:\Users\Administrator\Desktop\SepehrSmart_services
# python alwin_newSite_crawler_OK.py
import os.path
import os
import time
os.system("title Alwin Hotel Flask")
import json
import traceback
from app_crawl.hotel.Client_Dispatch_requests import executeRequest
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import json
import requests

import random
from concurrent.futures.thread import ThreadPoolExecutor
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)
executor=ThreadPoolExecutor(max_workers=50)
#==== capture captua ======
def get_cookie_selenium():
    from selenium import webdriver
    # from seleniumwire import webdriver
    from selenium.webdriver.common.by import By
    import time

    from aniti_captua import get_image_src,download_image,get_resolvedCaptua

    # from .aniti_captua import get_image_src,download_image,get_resolvedCaptua
    driver=webdriver.Chrome()

    driver.get('https://www.allwin24.ir')
    try:
        driver.find_element(By.XPATH,'//span[@id="close-popup"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//span[@onclick="showLoginContainer()"]').click()
    except:
        ''
    while(True):
        try:
            # driver.find_element(By.XPATH, '//span[@onclick="showLoginContainer()"]').click()
            driver.find_element(By.XPATH, '//input[@name="username"]').clear()
            driver.find_element(By.XPATH, '//input[@name="username"]').send_keys('mojalalsafarmhd@gmail.com')
            time.sleep(1)



            time.sleep(2)
            try:
                src=driver.find_element(By.XPATH, '//div[@id="captchaChild"]//img').get_property('src')
            except:
                driver.find_element(By.XPATH, '//button[@id="showCaptcha"]').click()
                time.sleep(2)
                src = driver.find_element(By.XPATH, '//div[@id="captchaChild"]//img').get_property('src')


            break
        except:
            time.sleep(2)


    # src=get_image_src()
    filename="alwin_captha.jpg"
    download_image(src,filename)
    captcha_text=get_resolvedCaptua(filename)
    print(captcha_text)

    driver.find_element(By.XPATH, '//input[@id="captchaCode"]').send_keys(captcha_text)
    time.sleep(2)

    driver.find_element(By.XPATH, '//input[@id="enterpassword"]').send_keys('@MST8451030yf')
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(2)
    # driver.find_element(By.XPATH, '//button[contains(text(),"جستجو")]').click()

    driver.find_element(By.XPATH,'//*[@id="flight-form"]/button').click()
    print('finish')
    # # Get cookies for the current domain
    cookies = driver.get_cookies()
    for cookie in cookies:
        print(f"Name: {cookie['name']}, Value: {cookie['value']}")


    import json
    with open('allwin_cookie.json','w',encoding='utf-8') as f:
        json.dump(cookies,f)
        f.close()
    driver.quit()



def convert_to_tooman(price) -> int:
    """
    convert rial price to tooman
    :param price: rial price
    :return: tooman price
    """
    return int(float(price) / 10)
#
# #-- get cookies
# for request in driver.requests:
#     if 'Client_User_Type' in request.url:  # for get rkey
#         # Check if the request has a response
#         if request.response:
#             print(f"Response Status Code: {request.response.status_code}")
#             print(f"Response Headers: {request.response.headers}")
#             try:
#                 # Print the response body if available
#                 response_body = request.response.body.decode('utf-8')
#                 print(f"Response Body: {response_body}")
#             except Exception as e:
#                 print(f"Error decoding response body: {e}")

#--- read cookies from file
def read_cookie_fromFile():

    # if os.path.exists('allwin_cookie.json'):
    with open('allwin_cookie.json','r',encoding='utf-8') as f:
        allwin_cookie_json=json.load(f)

    # else:  # create cookie
    desired_names = {'trackingid', 'rkey', 'monitoring_id'}
    cookies = {cookie['name']: cookie['value'] for cookie in allwin_cookie_json if cookie['name'] in desired_names}
    return cookies

def create_data_forHotel(data_json):
    import json
    from urllib.parse import urlencode
    # Prepare the dictionary for URL encoding
    data_dict_prepared = {
        key: json.dumps(value) if isinstance(value, dict) else value
        for key, value in data_json.items()
    }

    # Convert to query string
    query_string = urlencode(data_dict_prepared)

    # Replace '+' with spaces if necessary to match the desired format
    query_string = query_string.replace("+", " ")
    return query_string


def getHotelData(cookies,cityid,start_date,end_date,adultcount,
                 isAnalysis,hotelstarAnalysis,priorityTimestamp,use_cache):



    # cookies = {
    #     'rkey': 'FDD227FE-6E22-4C75-9EA0-6AA975CA527F',
    #     'monitoring_id': '677fe9d99daedc2b787cbcdc',
    #     'trackingid': '677fe9d99daedc2b787cbcdc',
    # }
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        # 'cookie': 'rkey=FDD227FE-6E22-4C75-9EA0-6AA975CA527F; monitoring_id=677fe9d99daedc2b787cbcdc; trackingid=677fe9d99daedc2b787cbcdc',
        'origin': 'https://www.allwin24.ir',
        'priority': 'u=1, i',
        'referer': 'https://www.allwin24.ir/Tem3_Hotel_Search.bc',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data_json = {
        "hotelid": "",
        "cityid": cityid,
        "fdate": start_date.replace('/', '-'),
        "tdate": end_date.replace('/', '-'),
        "rooms": {
            "rooms": [
                {
                    "adultcount": adultcount,
                    "childcountandage": "0"
                }
            ]
        },
        "sid": ""
    }

    query_string=create_data_forHotel(data_json)

    #---

    # --- With Execute Requests---
    req = executeRequest(method='post', url='https://www.allwin24.ir/Client_Hotel_Json.bc',
                         headers=headers,
                         cookies=cookies,
                         data=query_string,
                        priorityTimestamp=priorityTimestamp,
                        use_cache=use_cache)
                        # forceGet=1)
    req = json.loads(req)
    corrected_str = req['text'].replace("'", '"')
    res = json.loads(corrected_str)
    #_--
    return res

import re

def extract_capacity(room_name):

    if ('خواب' in room_name):  # moshkele: سوئیت یک خواب چهار تخت
        room_name=room_name.split('خواب')[1]


    # دیکشنری تبدیل کلمات فارسی به اعداد
    words_to_numbers = {
        'یک': 1,
        'دو': 2,
        'سه': 3,
        'چهار': 4,
        'پنج': 5,
        'شش': 6
    }

    # جستجوی اعداد عددی (1 تا 6) در رشته
    # numeric_match = re.search(r'\b([1-6]|[۱-۶])\b', room_name)  # پشتیبانی از اعداد فارسی و انگلیسی
    # numeric_match = re.search(r'([1-6]|[۱-۶])', room_name)

    matches = re.findall(r'([1-6]|[۱-۶])', room_name)
    last_match = matches[-1] if matches else None


    if last_match:
        return int(last_match)
        # return int(last_match.group())

    # جستجوی کلمات عددی فارسی (یک، دو، ...) در رشته
    for word, number in words_to_numbers.items():
        if word in room_name:
            return number

    return None  # اگر ظرفیتی پیدا نشد

#
# # لیست نمونه نام اتاق‌ها
# room_names = [
#     'اتاق دو تخته (اقامت با صبحانه)',
#     'اتاق 3 تخته',
#     'اتاق چهار نفره',
#     'اتاق 1 تخته',
#     'اتاق پنج تخته لوکس',
#     'اتاق شش نفره با امکانات کامل',
#     'اتاق ۲ تخته',
#     'اتاق یک نفره'
# ]
#
# # استخراج ظرفیت‌ها
# for room in room_names:
#     capacity = extract_capacity(room)
#     print(f"نام اتاق: {room} -> ظرفیت: {capacity}")
#



def get_room_data(start_date,end_date,hotelName,cookies,provider_id,dmnid,optionId):
    room_json={}
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        # 'cookie': 'rkey=FDD227FE-6E22-4C75-9EA0-6AA975CA527F; monitoring_id=677fe9d99daedc2b787cbcdc; trackingid=677fe9d99daedc2b787cbcdc',
        'origin': 'https://www.allwin24.ir',
        'priority': 'u=1, i',
        'referer': 'https://www.allwin24.ir/Tem3_Hotel_Search.bc',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = ('sid=&'
            f'mainprovider={{"provider_id":"{provider_id}","dmnid":{dmnid}}}&'
            f'optionId={optionId}')

    # while(True):
    tried=0
    while(True):
        try:


            #--- With Execute Requests---
            req = executeRequest(method='post', url='https://www.allwin24.ir/Client_Hotel_ShowAllRooms.bc',
                                 headers=headers,
                                 cookies=cookies,
                                 data=data)
                                 # priorityTimestamp=priorityTimestamp,
                                 # use_cache=0,
                                 # forceGet=1)
            # req = req.json()
            req = json.loads(req)
            corrected_str = req['text'].replace("'", '"')
            room_json = json.loads(corrected_str)
            #----

            #---------
            # response = requests.post('https://www.allwin24.ir/Client_Hotel_ShowAllRooms.bc', cookies=cookies, headers=headers, data=data)
            # corrected_str = response.text.replace("'", '"')
            # room_json=json.loads(corrected_str)
            #-------



            if 'families' not in room_json.keys():
                print(f'error in families --------- {hotelName} + -----{start_date} --- {end_date} -- tries =={tried}')
                if (tried>=3):
                    return False, hotelName, [], 0
                else:
                    time.sleep(random.randint(1,3))
                    tried=tried+1
                    continue

            break
        except Exception as e:
            print(f'get room error {hotelName}')
            tb = traceback.format_exc()
            print(f"An error occurred: {e}")
            print(f"Traceback details:\n{tb}")

            return False, hotelName, [], 0
            # time.sleep(random.randint(1, 3))
        # continue

    # --- print room names
    # print(' ------------- ')
    # print(hotelName)
    lst_rooms=[]
    min_price=0
    for roomItem in room_json['families']:
        avail=roomItem['availablerooms'][0]['info']['availability']
        if (avail!='available'):
            continue
        room={}
        board=''
        if ('board' in roomItem['availablerooms'][0]['info'].keys()):
            board=roomItem['availablerooms'][0]['info']['board']

        room['name']=roomItem['availablerooms'][0]['info']['room']+' '+board
        room['price']=convert_to_tooman(roomItem['totalCom'])

        #-- check cookie is valid:
        if (roomItem['totalCom']==roomItem['totalPrice']):
            return False,hotelName,[],0

        room['capacity']=roomItem['availablerooms'][0]['info']['adults']
        room['provider']="alwin"
        if (min_price==0):
            min_price=room['price']
        elif (room['price']<min_price):
            min_price=room['price']


        #---- room capaciity ---------
        room['capacity']=extract_capacity(room['name'])
        #-------------------------
        lst_rooms.append(room)

    print(f'hotel {hotelName} ----->  length={len(lst_rooms)} +--- WithTries == {tried}')
    return True,hotelName,lst_rooms,min_price


mapping_destination = {
    'THR': '1203548',
    'KIH': '1211110',
    'MHD': '1211083',
    'SYZ': '1211086',
    'IFN': '1211084',
    'TBZ': '1211085',
    'GSM': '1211111',
    'AWZ': '1211087',
    'BND': '1211127',
    'AZD': '1211090',
    'ZBR': '1211096',
    'KER': '1211091',
    'KSH': '1211115',
    'RAS': '1203561',
    'SRY': '1270513',
    'ABD': '1270534',
    'BUZ': '1211119',
    'GBT': '1270514',
    'OMH': '1211088',
    'ADU': '1211118',
    'HDM': '1211089',
    'RZR': '1211104',
    'KHD': '1211093',
    'NSH': '1211123',
    # ===========

}
from persiantools.jdatetime import JalaliDate
def convert_to_jalali(gregorian_date):

    year, month, day = map(int, gregorian_date.split('-'))

    jalali_date = JalaliDate.to_jalali(year, month, day)

    # Output the Persian date
    return jalali_date

#-------------------------------------------------------
#---- Get HotelData ---
#_-------------------------
import json
import requests
# get_cookie_selenium()


#---- parse HotelData
def get_hotels_info_writeJson(cityid, start_date, end_date, adultcount):
    """
    Fetches basic hotel information (name, star, IDs for room fetching)
    and saves it to a JSON file specific to the cityid.
    This mimics the approach in Booking_Hotel_flask_OK.py.
    """
    try:
        cookies = read_cookie_fromFile()
    except Exception as e:
        print(f'Error reading cookie file: {e}')
        # Handle cookie error appropriately, maybe try to regenerate or return empty
        return False # Indicate failure

    # Call getHotelData with necessary parameters (assuming it doesn't need all params like isAnalysis here)
    # You might need to adjust getHotelData if it strictly requires all parameters passed in get_hotels_old
    try:
        # Using placeholder values or None for parameters not directly needed for basic info fetching
        res = getHotelData(cookies=cookies, cityid=cityid, start_date=start_date, end_date=end_date, adultcount=adultcount,
                           isAnalysis=None, hotelstarAnalysis=None, # Or default values if needed by getHotelData
                           priorityTimestamp=time.time(), use_cache=True) # Example priority and cache settings
    except Exception as e:
        print(f"Error calling getHotelData: {e}")
        tb = traceback.format_exc()
        print(f"Traceback details:\n{tb}")
        return False # Indicate failure

    lst_hotel_info = [] # Changed from dictionary to list to match Booking approach
    # lst_futures = [] # Removed, room fetching happens later

    if not isinstance(res, list):
        print(f"Error: Expected a list from getHotelData, but got {type(res)}")
        # Potentially log the response `res` for debugging
        return False # Indicate failure

    for hotelItem in res:
        hotel = {}
        try:
            # Extract basic info
            # hotelID = hotelItem['id']['hotelId'] # Keep if needed, though Booking doesn't seem to use it directly later
            hotel['hotel_name'] = hotelItem['hotelinfo']['name']
            hotel['hotel_star'] = int(hotelItem['hotelinfo']['hotelsearch']['star'])
            hotel['provider'] = "alwin" # Add provider info
            hotel['min_price'] = 0 # Initialize min_price
            hotel['rooms'] = [] # Initialize rooms list

            # Extract parameters needed for get_room_data
            hotel['provider_id'] = hotelItem['id']['provider']['provider_id']
            hotel['dmnid'] = hotelItem['id']['provider']['dmnid']
            hotel['optionId'] = hotelItem['families'][0]['optionId'] # Assuming the first family's optionId is sufficient

            # Optional: Add a check/warning if multiple families exist, like before
            if len(hotelItem.get('families', [])) > 1:
                print(f'Warning: {hotel["hotel_name"]} has multiple families/optionIDs. Using the first one.')

            lst_hotel_info.append(hotel) # Add the hotel info dict to the list

            # Removed the executor submission for get_room_data
            # lst_futures.append(
            #     executor.submit(get_room_data, start_date, end_date, hotel['hotel_name'], cookies, provider_id, dmnid,
            #                     optionId))
            # lst_hotels[hotel['hotel_name']] = hotel # Removed dictionary storage

        except KeyError as e:
            print(f"KeyError processing hotel item: {e}. Item: {hotelItem}")
            # Decide whether to skip this hotel or stop the process
            continue # Skip this hotel and continue with the next
        except Exception as e:
            print(f"Unexpected error processing hotel item: {e}. Item: {hotelItem}")
            tb = traceback.format_exc()
            print(f"Traceback details:\n{tb}")
            continue # Skip this hotel

    # Create directory if it doesn't exist
    info_dir = 'Alwin_hotels'
    if not os.path.exists(info_dir):
        try:
            os.makedirs(info_dir)
            print(f"Created directory: {info_dir}")
        except OSError as e:
            print(f"Error creating directory {info_dir}: {e}")
            return False # Indicate failure

    # Write the list of hotel info to a JSON file
    info_filename = os.path.join(info_dir, f'Alwin_hotel_info_{cityid}.json')
    try:
        with open(info_filename, 'w', encoding='utf-8') as f:
            json.dump(lst_hotel_info, f, ensure_ascii=False, indent=4)
        print(f"Successfully wrote hotel info to {info_filename}")
        return True # Indicate success
    except IOError as e:
        print(f"Error writing hotel info to {info_filename}: {e}")
        return False # Indicate failure
    except Exception as e:
        print(f"Unexpected error writing JSON file: {e}")
        return False # Indicate failure


# def get_hotels_old(cityid,start_date,end_date,adultcount,isAnalysis,hotelstarAnalysis,priorityTimestamp,use_cache):
def get_hotels(cityid, start_date, end_date, adultcount, isAnalysis, hotelstarAnalysis, priorityTimestamp, use_cache):
    """
    Fetches hotel data and handles analysis mode differently:
    - For isAnalysis=0: Fetches fresh data from API
    - For isAnalysis=1: Uses cached data from Redis
    """
    try:
        cookies = read_cookie_fromFile()
    except Exception as e:
        print(f'Error reading cookie file: {e}')
        if not redis_client.exists('Get_cookies_Done'):
            redis_client.set('Fetch_Cookie_Alwin', '1')
        return []

    hotels_info = []
    # Include more parameters in Redis key pattern
    redis_key_pattern = f"alwin:hotel:{cityid}:{start_date}:{end_date}:{adultcount}:*"

    # Different behavior based on isAnalysis
    if isAnalysis == '1' or isAnalysis is True:
        print("Analysis mode: Using cached hotel data from Redis")
        # Get all hotel keys for this city and parameters
        all_keys = redis_client.keys(redis_key_pattern)
        
        for key in all_keys:
            try:
                hotel_data = redis_client.get(key)
                if hotel_data:
                    hotel_info = json.loads(hotel_data)
                    hotels_info.append(hotel_info)
            except Exception as e:
                print(f"Error reading hotel data from Redis: {e}")
                continue
                
        if not hotels_info:
            print("No cached hotel data found in Redis, fetching fresh data...")
            try:
                hotels_data = getHotelData(
                    cookies=cookies,
                    cityid=cityid,
                    start_date=start_date,
                    end_date=end_date,
                    adultcount=adultcount,
                    isAnalysis=isAnalysis,
                    hotelstarAnalysis=hotelstarAnalysis,
                    priorityTimestamp=priorityTimestamp,
                    use_cache=use_cache
                )

                # Process hotels and store in Redis
                redis_pipe = redis_client.pipeline()
                
                for hotel in hotels_data:
                    try:
                        hotel_info = {
                            'hotelId': hotel['id']['hotelId'],
                            'hotel_name': hotel['hotelinfo']['name'],
                            'hotel_star': int(hotel['hotelinfo']['hotelsearch']['star']),
                            'provider': 'alwin',
                            'min_price': 0,
                            'rooms': [],
                            'provider_id': hotel['id']['provider']['provider_id'],
                            'dmnid': hotel['id']['provider']['dmnid'],
                            'optionId': hotel['families'][0]['optionId'] if hotel.get('families') else None
                        }
                        
                        # Store complete hotel info in Redis with new key pattern
                        redis_key = f"alwin:hotel:{cityid}:{start_date}:{end_date}:{adultcount}:{hotel_info['hotelId']}"
                        redis_pipe.set(redis_key, json.dumps(hotel_info), ex=10*60)  # expire in 1 hour
                        hotels_info.append(hotel_info)
                        
                    except Exception as e:
                        print(f"Error processing hotel: {e}")
                        continue

                # Execute Redis pipeline
                try:
                    redis_pipe.execute()
                except Exception as e:
                    print(f"Error storing hotel data in Redis: {e}")
                    
            except Exception as e:
                print(f"Error fetching hotel data: {e}")
                return []
    else:
        print("Normal (RAASII) mode: Fetching fresh hotel data")
        # Fetch hotels directly using getHotelData
        try:
            hotels_data = getHotelData(
                cookies=cookies,
                cityid=cityid,
                start_date=start_date,
                end_date=end_date,
                adultcount=adultcount,
                isAnalysis=isAnalysis,
                hotelstarAnalysis=hotelstarAnalysis,
                priorityTimestamp=priorityTimestamp,
                use_cache=use_cache
            )
        except Exception as e:
            print(f"Error fetching hotel data: {e}")
            return []

        # Process hotels and store in Redis
        redis_pipe = redis_client.pipeline()
        
        for hotel in hotels_data:
            try:
                hotel_info = {
                    'hotelId': hotel['id']['hotelId'],
                    'hotel_name': hotel['hotelinfo']['name'],
                    'hotel_star': int(hotel['hotelinfo']['hotelsearch']['star']),
                    'provider': 'alwin',
                    'min_price': 0,
                    'rooms': [],
                    'provider_id': hotel['id']['provider']['provider_id'],
                    'dmnid': hotel['id']['provider']['dmnid'],
                    'optionId': hotel['families'][0]['optionId'] if hotel.get('families') else None
                }
                
                # Store complete hotel info in Redis
                redis_key = f"alwin:hotel:{cityid}:{start_date}:{end_date}:{adultcount}:{hotel_info['hotelId']}"
                redis_pipe.set(redis_key, json.dumps(hotel_info), ex=10*60)  # expire in 1 hour
                hotels_info.append(hotel_info)
                
            except Exception as e:
                print(f"Error processing hotel: {e}")
                continue

        # Execute Redis pipeline
        try:
            redis_pipe.execute()
        except Exception as e:
            print(f"Error storing hotel data in Redis: {e}")

    # Filter hotels based on analysis criteria
    if isAnalysis == '1' or isAnalysis is True:
        filtered_hotels = [
            hotel for hotel in hotels_info
            if str(hotel['hotel_star']) in hotelstarAnalysis
            or hotel['hotel_name'] in hotelstarAnalysis
        ]
        print(f'Alwin Analysis: Filtered to {len(filtered_hotels)} hotels')
        if not filtered_hotels:
            return []
    else:
        filtered_hotels = hotels_info

    # Fetch room data for filtered hotels
    lst_hotels = {hotel['hotelId']: hotel for hotel in filtered_hotels}
    futures = []
    
    for hotel in filtered_hotels:
        try:
            futures.append(
                executor.submit(
                    get_room_data,
                    start_date,
                    end_date,
                    hotel['hotel_name'],
                    cookies,
                    hotel['provider_id'],
                    hotel['dmnid'],
                    hotel['optionId']
                )
            )
        except Exception as e:
            print(f"Error submitting room data task for {hotel['hotel_name']}: {e}")
            continue

    # Process room data results
    is_live_cookie = 0
    for future in futures:
        try:
            cookie_status, hotelName, rooms, min_price = future.result()
            
            # Find hotel by name in lst_hotels
            for hotel in lst_hotels.values():
                if hotel['hotel_name'] == hotelName:
                    hotel['rooms'] = rooms
                    hotel['min_price'] = min_price
                    break

            if cookie_status:
                is_live_cookie = 1

        except Exception as e:
            print(f"Error processing room data result: {e}")
            continue

    # Handle dead cookie
    if is_live_cookie == 0 and futures:
        if not redis_client.exists('Get_cookies_Done'):
            redis_client.set('Fetch_Cookie_Alwin', '1')

    return list(lst_hotels.values())


@app.route('/alwin_hotels', methods=['GET'])
def alwin_hotels():
    start_date = request.args.get('startdate')
    end_date = request.args.get('end_date')
    adults = request.args.get('adults')
    destination = request.args.get('target')


    isAnalysis=request.args.get('isAnalysis')

    hotelstarAnalysis=request.args.get('hotelstarAnalysis')
    hotelstarAnalysis=json.loads(hotelstarAnalysis)
    priorityTimestamp = request.args.get('priorityTimestamp')
    use_cache=request.args.get('use_cache')



    post_header = {
        'Content-Type': 'application/json',
        "authorization": ""
    }

    start_date=str(convert_to_jalali(start_date))
    end_date = str(convert_to_jalali(end_date))
    # # self.executor = ThreadPoolExecutor(max_workers=100)
    try:
        # hotels = get_hotels(end_date, destination, adults, start_date, post_header) # Original line commented out
        cityid=mapping_destination[destination]
        # Ensure isAnalysis is treated as boolean or '0'/'1' consistently
        is_analysis_flag = isAnalysis == '1' or isAnalysis == True

        # Call the renamed and refactored get_hotels function
        hotels = get_hotels(
            cityid=cityid,
            start_date=start_date,
            end_date=end_date,
            adultcount=adults,
            isAnalysis=is_analysis_flag, # Pass the processed flag
            hotelstarAnalysis=hotelstarAnalysis,
            priorityTimestamp=priorityTimestamp,
            use_cache=use_cache
        )
        # hotels=list(hotels.values()) # No longer needed as get_hotels returns a list

        # Return the list of hotels as a JSON response
        return jsonify(hotels)

    except KeyError:
         print(f"Error: Invalid destination key '{destination}'")
         return jsonify({"error": f"Invalid destination key: {destination}"}), 400
    except Exception as e: # Catch broader exceptions during the process
        print(f"An error occurred in /alwin_hotels route: {e}")
        tb = traceback.format_exc()
        print(f"Traceback details:\n{tb}")
        return jsonify({"error": "An internal server error occurred"}), 500 # Return a generic error



#========= Keep Alive cookie=======
import threading
# import time # Already imported globally
# import os # Already imported globally
def task():
    """
    Background task to check cookie status and regenerate if necessary.
    Triggers selenium if 'allwin_cookie.json' is missing or if 'Fetch_Cookie_Alwin'
    flag is set in Redis, ensuring 'Get_cookies_Done' lock is not present.
    """
    while True:
        print("Background task checking cookie status...")
        cookie_file_path = 'allwin_cookie.json'
        cookie_file_exists = os.path.exists(cookie_file_path)
        fetch_cookie_flag = redis_client.exists('Fetch_Cookie_Alwin')
        cookie_being_fetched = redis_client.exists('Get_cookies_Done') # Check if selenium is already running/locked

        should_fetch = False
        if not cookie_being_fetched:
            if fetch_cookie_flag:
                print("Detected 'Fetch_Cookie_Alwin' flag.")
                should_fetch = True
            elif not cookie_file_exists:
                print(f"Cookie file '{cookie_file_path}' not found.")
                should_fetch = True
        else:
            print("Cookie fetch already in progress ('Get_cookies_Done' exists). Skipping check.")

        if should_fetch:
            print("Attempting to fetch new cookies using Selenium...")
            try:
                # Set lock *before* running the potentially long selenium task
                # Use a timeout (e.g., 10 minutes) in case selenium hangs
                redis_client.set('Get_cookies_Done', '1', ex=10*60)
                get_cookie_selenium() # This function writes the cookie file
                print("Selenium task finished successfully.")
                # Clear the trigger flag only on success
                if fetch_cookie_flag:
                    redis_client.delete('Fetch_Cookie_Alwin')
                # Lock ('Get_cookies_Done') will expire based on 'ex'
            except Exception as e:
                print(f"Error running get_cookie_selenium: {e}")
                tb = traceback.format_exc()
                print(f"Traceback details:\n{tb}")
                # Remove the lock immediately on error to allow retries sooner
                # Otherwise, it would wait for the 10-minute timeout
                redis_client.delete('Get_cookies_Done')
            # No finally block needed here, lock handled by timeout or explicit delete on error

        else:
            # Optional: Add a message if no action is needed
            if not cookie_being_fetched:
                 print("Cookie status OK (file exists, no fetch flag).")

        print("Background task sleeping...")
        # Adjust sleep time as needed
        sleep_duration = random.randint(30, 90) # Check every 30-90 seconds
        time.sleep(sleep_duration)
        # time.sleep(random.randint(10,60))  # Original shorter sleep
        # time.sleep(30*60) # Original longer sleep

# Ensure the thread starts after the function definition
thread = threading.Thread(target=task, daemon=True)
thread.start()

#-------------------------------

if __name__ == '__main__':

    # --- Add code here to pre-generate hotel info files ---
    print("Starting initial hotel info generation...")
    # Define default dates/adults for info generation if needed
    from datetime import datetime, timedelta
    default_start_date = (datetime.today() + timedelta(days=10)).strftime('%Y-%m-%d')
    default_end_date = (datetime.today() + timedelta(days=13)).strftime('%Y-%m-%d')
    default_adults = '2'

    # Convert to Jalali for Alwin service
    jalali_start_date = str(convert_to_jalali(default_start_date))
    jalali_end_date = str(convert_to_jalali(default_end_date))


    for dest_code, city_id in mapping_destination.items():
        print(f"Generating info for {dest_code} (ID: {city_id})...")
        # Check if file already exists to avoid unnecessary calls (optional)
        info_dir = 'Alwin_hotels'
        info_filename = os.path.join(info_dir, f'Alwin_hotel_info_{city_id}.json')
        if os.path.exists(info_filename):
             print(f"Info file already exists: {info_filename}. Skipping generation.")
             continue

        success = get_hotels_info_writeJson(
            cityid=city_id,
            start_date=jalali_start_date,
            end_date=jalali_end_date,
            adultcount=default_adults
        )
        if success:
            print(f"Successfully generated info for {dest_code}")
        else:
            print(f"Failed to generate info for {dest_code}")
        time.sleep(random.randint(1, 3)) # Add a small delay between destinations

    print("Initial hotel info generation complete.")
    # ----------------------------------------------------

    # app.run(debug=True,host='0.0.0.0',port=5001)
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5055) # Use threaded=True if needed, default is False




