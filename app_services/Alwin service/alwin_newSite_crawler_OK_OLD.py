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
redis_client = redis.Redis(host='localhost', port=6379, db=0)
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
    response = requests.post('https://www.allwin24.ir/Client_Hotel_Json.bc', cookies=cookies, headers=headers,
                             data=query_string)

    corrected_str = response.text.replace("'", '"')
    res=json.loads(corrected_str)
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
                                 data=data,
                                 # priorityTimestamp=priorityTimestamp,
                                 use_cache=1)
                                 # forceGet=force)
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

#-------------------------------------------------------
#---- Get HotelData ---
#_-------------------------
import json
import requests
# get_cookie_selenium()


#---- parse HotelData
def get_hotels_info_writeJson():
    try:
        cookies=read_cookie_fromFile()
    except:
        print('error in reading cookie file')
        cookies=''
        # res=getHotelData(cookies=cookies,cityid='1211110',start_date='1403-10-29',end_date='1403-11-3',adultcount=2)
    res = getHotelData(cookies=cookies, cityid=cityid, start_date=start_date, end_date=end_date, adultcount=adultcount,
                       isAnalysis=isAnalysis, hotelstarAnalysis=hotelstarAnalysis,
                       priorityTimestamp=priorityTimestamp, use_cache=use_cache)
    lst_hotels = {}
    lst_futures = []
    for hotelItem in res:
        hotel = {}
        try:
            hotelID = hotelItem['id']['hotelId']
            hotel['hotel_name'] = hotelItem['hotelinfo']['name']
            hotel['hotel_star'] = int(hotelItem['hotelinfo']['hotelsearch']['star'])

            provider_id = hotelItem['id']['provider']['provider_id']
            dmnid = hotelItem['id']['provider']['dmnid']
            # optionId=hotel['infoForMapping']['all_offers'][f'{provider_id}-{dmnid}'][0]['optionId']
            optionId = hotelItem['families'][0]['optionId']

            # print(f'len optionID === {len(hotelItem['families'])}')
            if (len(hotelItem['families'])) > 1:
                print(f'{hotel["hotel_name"]} ----------- chand optionID')

            # -- standalone
            # cookieStatus,lst_rooms,min_price=get_room_data(cookies, provider_id, dmnid, optionId)
            # --parallel
            lst_futures.append(
                executor.submit(get_room_data, start_date, end_date, hotel['hotel_name'], cookies, provider_id, dmnid,
                                optionId))
            lst_hotels[hotel['hotel_name']] = hotel
        except:
            continue




def get_hotels_old(cityid,start_date,end_date,adultcount,isAnalysis,hotelstarAnalysis,priorityTimestamp,use_cache):
    try:
        cookies=read_cookie_fromFile()
    except:
        print('error in reading cookie file')
        cookies=''
    # res=getHotelData(cookies=cookies,cityid='1211110',start_date='1403-10-29',end_date='1403-11-3',adultcount=2)
    res = getHotelData(cookies=cookies, cityid=cityid, start_date=start_date, end_date=end_date, adultcount=adultcount,
                       isAnalysis=isAnalysis,hotelstarAnalysis=hotelstarAnalysis,
                       priorityTimestamp=priorityTimestamp,use_cache=use_cache)
    lst_hotels={}
    lst_futures=[]
    for hotelItem in res:
        hotel={}
        try:
            hotelID=hotelItem['id']['hotelId']
            hotel['hotel_name']=hotelItem['hotelinfo']['name']
            hotel['hotel_star']=int(hotelItem['hotelinfo']['hotelsearch']['star'])

            provider_id=hotelItem['id']['provider']['provider_id']
            dmnid = hotelItem['id']['provider']['dmnid']
            # optionId=hotel['infoForMapping']['all_offers'][f'{provider_id}-{dmnid}'][0]['optionId']
            optionId = hotelItem['families'][0]['optionId']

            # print(f'len optionID === {len(hotelItem['families'])}')
            if (len(hotelItem['families']))>1:
                print(f'{hotel["hotel_name"]} ----------- chand optionID')

            # -- standalone
            # cookieStatus,lst_rooms,min_price=get_room_data(cookies, provider_id, dmnid, optionId)
            #--parallel
            lst_futures.append(executor.submit(get_room_data,start_date,end_date,hotel['hotel_name'],cookies, provider_id, dmnid, optionId))
            lst_hotels[hotel['hotel_name']]=hotel
        except:
            continue


    results_room=[]
    is_live_cookie=0
    for future in lst_futures:
        try:
            result=future.result()
            results_room.append(result)
            # True, hotelName, lst_rooms, min_price

            hotelName=result[1]
            lst_hotels[hotelName]['rooms']=result[2]
            lst_hotels[hotelName]['provider'] = "alwin"
            lst_hotels[hotelName]['min_price'] = result[3]

            #---- check redis for selenium
            if (result[0]==True): # live cookie
                is_live_cookie=1
                # redis_client.delete('Get_cookies_Done')
            #-----

        except Exception as e:
            print(f'error occured fetchin room {hotelName}  error= =====  {e}')
            tb = traceback.format_exc()
            print(f"An error occurred: {e}")
            print(f"Traceback details:\n{tb}")

    if (is_live_cookie==0):
        if (redis_client.exists('Get_cookies_Done')):
            print('Cookie is dead! -- not insert into Redis')
            return []
        else:
            redis_client.set('Fetch_Cookie_Alwin', '1')
            print('Cookie is dead!')
            time.sleep(random.randint(1, 5))
            return []
    return lst_hotels

from persiantools.jdatetime import JalaliDate
def convert_to_jalali(gregorian_date):

    year, month, day = map(int, gregorian_date.split('-'))

    jalali_date = JalaliDate.to_jalali(year, month, day)

    # Output the Persian date
    return jalali_date


#========= Keep Alive cookie=======
import threading
import time
def task():
    while True:
        print("Task is running...")
        if (redis_client.exists('Fetch_Cookie_Alwin') and not redis_client.exists('Get_cookies_Done')):
            get_cookie_selenium()
            redis_client.set('Get_cookies_Done', '1',ex=10*60) # 10 minutes
            redis_client.delete('Fetch_Cookie_Alwin')
        print("Sleeping ...")
        time.sleep(random.randint(10,60))  # Wait for 30 minutes (30 * 60 seconds)
        # time.sleep(30*60)
thread = threading.Thread(target=task, daemon=True)
thread.start()

#-------------------------------


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
        # hotels = get_hotels(end_date, destination, adults, start_date, post_header)
        cityid=mapping_destination[destination]
        hotels=get_hotels(cityid, start_date, end_date, adults,isAnalysis,hotelstarAnalysis,priorityTimestamp,use_cache)
        hotels=list(hotels.values())
        # Return the list of hotels as a JSON response
        return jsonify(hotels)

    except:
        return []



if __name__ == '__main__':

    # app.run(debug=True,host='0.0.0.0',port=5001)
    app.run(host='0.0.0.0',port=5055)




