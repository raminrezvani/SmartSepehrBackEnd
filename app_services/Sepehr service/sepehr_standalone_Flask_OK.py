import requests
import urllib3
import random
import os
from pathlib import Path
from datetime import datetime
import hashlib  # Add this import
from requests import request

from app_crawl.helpers import ready_price, convert_to_tooman, convert_gregorian_date_to_persian
from bs4 import BeautifulSoup
# from app_crawl.insert_influx import Influxdb
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
# from django.conf import settings
import redis

# redis_client = redis.Redis(
#     host=settings.REDIS_CONFIG['HOST'],
#     port=settings.REDIS_CONFIG['PORT'],
#     db=settings.REDIS_CONFIG['DB'],
#     decode_responses=settings.REDIS_CONFIG['DECODE_RESPONSES']
# )

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = Path(__file__).resolve().parent
# influx = Influxdb()

def calculate_night_count(start_date, end_date):
    return (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days

# Add this import at the top of the file
from app_crawl.hotel.Client_Dispatch_requests import executeRequest

# Add these imports at the top of the file
from flask import Flask, request, jsonify


# Add these functions after the imports and before get_data function
def generate_redis_key(target, start_date, end_date, provider_name):
    """Generate an optimized Redis key using MD5 hash"""
    key_string = f"{target}_{start_date}_{end_date}_{provider_name}"
    return f"sepehr_hotel:{hashlib.md5(key_string.encode()).hexdigest()}"

def generate_hotels_cache_key(target, start_date, provider_name):
    """Generate Redis key for processed hotels cache"""
    key_string = f"processed_{target}_{start_date}_{provider_name}"
    return f"sepehr_processed:{hashlib.md5(key_string.encode()).hexdigest()}"

# Add after generate_hotels_cache_key function and before get_data function
def process_hotel(hotel, provider_name) -> dict:
    """Process a single hotel and return its data"""
    try:
        hotel_star = hotel.select_one('img[alt*="ستاره"]').get('alt').replace('ستاره', '').replace('هتل', '').strip()
        hotel_name = hotel.select_one("tr.header td:nth-child(1)").text.strip()

        appended_item = {
            "hotel_name": hotel_name,
            "hotel_star": hotel_star,
            "min_price": None,
            "rooms": [],
            "provider": provider_name
        }

        rooms = hotel.select('.input_hand label')
        room_row = hotel.select("tr[bgcolor='#EEEEEE']:has(.input_hand)")

        for index, room in enumerate(rooms):
            room_price = ready_price(room_row[index].select_one("td:nth-child(4)").text.strip())

            try:
                room_status = room_row[index].select_one("td:nth-child(7)").text.strip()
                if 'تلفن' in room_status:
                    continue

                try:
                    room_status = room_row[index].select_one("font[color='red']").text.strip()
                    continue
                except:
                    pass
            except:
                continue

            room_price = convert_to_tooman(room_price)
            room_item = {
                "name": room.text.strip(),
                "capacity": len(room_row[index].select("td:nth-child(5) i")),
                "price": room_price,
                "status": room_status,
                "provider": provider_name
            }

            if not appended_item['min_price']:
                appended_item['min_price'] = room_price
            if room_price < appended_item['min_price']:
                appended_item['min_price'] = room_price

            appended_item['rooms'].append(room_item)

        appended_item['rooms'] = sorted(appended_item['rooms'], key=lambda k: k['price'])
        return appended_item
    except Exception as e:
        print(f"Error processing hotel: {str(e)}")
        return None

def get_data(target, start_date, end_date, adults, cookie, provider_name, priorityTimestamp):
    try:
        # Validate cookie structure
        if not cookie or not isinstance(cookie, dict):
            print("Invalid cookie format")
            return None
            
        if 'hotel' not in cookie or target not in cookie['hotel']:
            print(f"Missing hotel or target data in cookie for {target}")
            return None

        if 'cookie' not in cookie['hotel'][target]:
            print(f"Missing cookie data for target {target}")
            return None

        cookies = cookie['hotel'][target]['cookie']
        if not cookies:
            print("No cookies found")
            return None

        # Validate required cookie fields
        required_fields = ['domain']  # domain in root level of cookie
        required_hotel_fields = ['view_state', 'view_state_generator', 'event_validation']  # these fields should be in cookie['hotel']
        
        for field in required_fields:
            if field not in cookie:
                print(f"Missing required field in cookie root: {field}")
                return None
                
        for field in required_hotel_fields:
            if field not in cookie['hotel']:
                print(f"Missing required field in cookie['hotel']: {field}")
                return None

        rnd = random.randint(1550000000000000, 1560000000000009)

        headers = {
            'authority': cookie['domain'],
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'cache-control': 'max-age=0',
            'origin': f'https://{cookie["domain"]}',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        params = {
            'action': 'display',
            'rnd': rnd,
        }

        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': cookie['hotel']['view_state'],
            '__VIEWSTATEGENERATOR': cookie['hotel']['view_state_generator'],
            '__EVENTVALIDATION': cookie['hotel']['event_validation'],
            'dplTo': target,
            'dplHotelName': '0',
            'txtCheckinDate': convert_gregorian_date_to_persian(start_date, "%Y/%m/%d")['date'],
            'dplNights': calculate_night_count(start_date, end_date),
            'btnSearch': 'جستجو',
            'dplRoom1Adults': '0',
            'dplRoom1Childs': '0',
            'dplRoom2Adults': '0',
            'dplRoom2Childs': '0',
            'dplRoom3Adults': '0',
            'dplRoom3Childs': '0',
            'dplRoom4Adults': '0',
            'dplRoom4Childs': '0',
            'dplRoom5Adults': '0',
            'dplRoom5Childs': '0',
            'dplRoom6Adults': '0',
            'dplRoom6Childs': '0',
            'dplRoom7Adults': '0',
            'dplRoom7Childs': '0',
            'dplRoom8Adults': '0',
            'dplRoom8Childs': '0',
            'dplRoom9Adults': '0',
            'dplRoom9Childs': '0',
            'dplRoom10Adults': '0',
            'dplRoom10Childs': '0',
        }

        # First request
        post_response = requests.post(
            f'https://{cookie["domain"]}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        )
        
        if not post_response.ok:
            print(f"POST request failed with status code: {post_response.status_code}")
            return None

        # Second request
        res = requests.get(
            f"https://{cookie['domain']}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx?action=display&rnd={rnd}",
            cookies=cookies,
            verify=False
        )

        if not res.ok:
            print(f"GET request failed with status code: {res.status_code}")
            return None

        return res.text

    except Exception as e:
        print(f"Error in get_data: {str(e)}")
        return None

def get_result(target, start_date, end_date, adults, cookie, provider_name, isAnalysis, hotelstarAnalysis=[], priorityTimestamp=1):
    t1 = datetime.now()
    try:
        redis_key_db = generate_redis_key(target, start_date, end_date, provider_name)
        processed_hotels_key = generate_hotels_cache_key(target, start_date, provider_name)
        
        # Get both raw and processed data in one Redis call
        with redis_client.pipeline() as pipe:
            pipe.get(redis_key_db)
            pipe.get(processed_hotels_key)
            redis_data, processed_hotels_data = pipe.execute()
            
        # If we have processed hotels data, use it directly
        if processed_hotels_data:
            print('------ Processed Hotels Cache Hit -----')
            all_processed_hotels = json.loads(processed_hotels_data)
            
        # Only process HTML if we don't have processed data
        else:
            if redis_data:
                print('------ Sepehr Cache Hit -----')
                data = json.loads(redis_data)
            else:
                data = get_data(target, start_date, end_date, adults, cookie, provider_name, priorityTimestamp)
                if not data:
                    return {'status': False, "data": [], 'message': "خطا در دریافت اطلاعات"}
                # Cache raw HTML data
                redis_client.setex(redis_key_db, 5*60, json.dumps(data))

            # Process HTML only if we don't have processed data
            soup = BeautifulSoup(data, 'html.parser')
            hotels = soup.select("table.Table03:has(tr.header)")
            
            # Process all hotels in parallel
            with ThreadPoolExecutor(max_workers=max(1, min(20, len(hotels)))) as executor:
                future_to_hotel = {
                    executor.submit(process_hotel, hotel, provider_name): hotel 
                    for hotel in hotels
                }
                
                all_processed_hotels = []
                for future in as_completed(future_to_hotel):
                    hotel_data = future.result()
                    if hotel_data:
                        all_processed_hotels.append(hotel_data)
            
            # Cache processed hotels data
            if all_processed_hotels:
                redis_client.setex(processed_hotels_key, 5*60, json.dumps(all_processed_hotels))

        # Filter hotels based on analysis criteria
        if isAnalysis and all_processed_hotels:
            hotel_names = {hotel["hotel_name"] for hotel in all_processed_hotels}
            selected_hotels = set()
            
            # Get all hotel mappings in one Redis call
            with redis_client.pipeline() as pipe:
                for hotel_star in hotelstarAnalysis:
                    pipe.get(f"asli_hotel:{hotel_star}")
                redis_results = pipe.execute()
                
                # Process mappings
                for redis_data in redis_results:
                    if redis_data:
                        mapped_hotels = json.loads(redis_data)
                        selected_hotels.update(hotel_name for hotel_name in mapped_hotels if hotel_name in hotel_names)
            
            result = [hotel for hotel in all_processed_hotels if hotel["hotel_name"] in selected_hotels]
        else:
            result = all_processed_hotels

        spendTime = (datetime.now() - t1).total_seconds()
        print(f'{provider_name} ---- Total Processing Time_{start_date} --- {spendTime}')
        
        return result

    except Exception as e:
        print(f"Error in get_result: {str(e)}")
        return {'status': False, "data": [], 'message': "اتمام زمان"}

# Add after existing imports
app = Flask(__name__)

# Add new endpoint
@app.route('/api/hotel/search', methods=['POST'])
def search_hotels():
    try:
        data = request.get_json()
        
        # Extract required parameters from request
        target = data.get('target')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        adults = data.get('adults')
        cookie = data.get('cookie')
        provider_name = data.get('provider_name')
        is_analysis = data.get('is_analysis', False)
        hotelstar_analysis = data.get('hotelstar_analysis', [])
        priority_timestamp = data.get('priority_timestamp', 1)

        # Validate required parameters
        if not all([target, start_date, end_date, cookie, provider_name]):
            return jsonify({
                'status': False,
                'message': 'Missing required parameters',
                'data': []
            }), 400

        # Use existing get_result function
        result = get_result(
            target=target,
            start_date=start_date,
            end_date=end_date,
            adults=adults,
            cookie=cookie,
            provider_name=provider_name,
            isAnalysis=is_analysis,
            hotelstarAnalysis=hotelstar_analysis,
            priorityTimestamp=priority_timestamp
        )

        if isinstance(result, dict) and 'status' in result:
            return jsonify(result), 400

        return jsonify({
            'status': True,
            'data': result,
            'message': 'Success'
        })

    except Exception as e:
        return jsonify({
            'status': False,
            'message': str(e),
            'data': []
        }), 500

# Add at the end of the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
