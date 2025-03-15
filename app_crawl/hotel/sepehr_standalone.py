import urllib3
import random
import os
from pathlib import Path
from datetime import datetime

from requests import request
from app_crawl.helpers import ready_price, convert_to_tooman, convert_gregorian_date_to_persian
from bs4 import BeautifulSoup
from app_crawl.insert_influx import Influxdb

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = Path(__file__).resolve().parent
influx = Influxdb()

def calculate_night_count(start_date, end_date):
    return (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days

def get_data(target, start_date, end_date, adults, cookie, provider_name):
    try:
        cookies = cookie['hotel'][target]['cookie']
    except:
        return False

    if not cookies:
        return False

    rnd = random.randint(1550000000000000, 1560000000000009)

    headers = {
        'authority': cookie['domain'],
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'origin': f'https://{cookie["domain"]}',
        'referer': f'https://{cookie["domain"]}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx?action=display&rnd={rnd}',
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

    request(
        "POST",
        f'https://{cookie["domain"]}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    influx.capture_logs(1, 'sepehr')

    res = request(
        "GET",
        f"https://{cookie['domain']}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx?action=display&rnd={rnd}",
        cookies=cookies,
        verify=False
    )
    influx.capture_logs(1, 'sepehr')

    return res.text

def get_static_data():
    with open('/Users/javad/Projects/hotel_providers_api/app_crawl/hotel/test.html', 'r') as html_file:
        data = html_file.read()
    return data

def add_to_file(provider_name, start_date, data):
    try:
        file_name = f'{provider_name}_{start_date.replace("/", "_")}.html'
        path_file = os.path.join(BASE_DIR, 'logs', file_name)
        with open(path_file, 'w', encoding="UTF-8") as html_file:
            html_file.write(data)
        return True
    except:
        return False

def get_result(target, start_date, end_date, adults, cookie, provider_name, isAnalysis, hotelstarAnalysis=[],priorityTimestamp=1):
    t1 = datetime.now()
    try:
        data = get_data(target, start_date, end_date, adults, cookie, provider_name)
        spendTime = (datetime.now() - t1).total_seconds()
        print(f'{provider_name} ---- GetData_{start_date} --- {spendTime}')

        t1 = datetime.now()
        soup = BeautifulSoup(data, 'html.parser')
        result = []
    except:
        return {'status': False, "data": [], 'message': "اتمام زمان"}

    hotels = soup.select("table.Table03:has(tr.header)")

    for hotel in hotels:
        try:
            hotel_star = hotel.select_one('img[alt*="ستاره"]').get('alt').replace('ستاره', '').replace('هتل', '').strip()

            # ======== Check for 5-Star hotels
            if isAnalysis and str(hotel_star) not in hotelstarAnalysis:
                continue
            #-----------

            appended_item = {
                "hotel_name": hotel.select_one("tr.header td:nth-child(1)").text.strip(),
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
                        room_status = "تماس تلفنی"
                        continue

                    try:
                        room_status = room_row[index].select_one("font[color='red']").text.strip()
                        room_status = "تماس تلفنی"
                        continue
                    except:
                        pass
                except:
                    room_status = "تماس تلفنی"
                    # ===========
                    # Skipp tamas telefoni
                    # ============
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
            result.append(appended_item)

        except:
            print(f"{provider_name} hotel wrong")

    spendTime = (datetime.now() - t1).total_seconds()
    print(f'{provider_name} ---- ParseData_{start_date} --- {spendTime}')

    return result
