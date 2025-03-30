import urllib3
import random
import os
from pathlib import Path
from datetime import datetime
import json

from requests import request
from app_crawl.helpers import ready_price, convert_to_tooman, convert_gregorian_date_to_persian
from bs4 import BeautifulSoup
from app_crawl.insert_influx import Influxdb
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = Path(__file__).resolve().parent


# def sepehr_get_data(target, start_date, end_date, adults, cookie, provider_name,isAnalysiss,hotelstarAnalysis=[]):
#
#     pass

class SepehrHotel:
    def __init__(self, target, start_date, end_date, adults, cookie, provider_name,isAnalysiss,hotelstarAnalysis=[]):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_persian = convert_gregorian_date_to_persian(start_date, "%Y/%m/%d")['date']
        self.target = target
        self.adults = adults
        self.cookies = cookie
        self.provider_name = provider_name
        # self.isAnalysis=isAnalysiss

        self.isAnalysis=isAnalysiss[0] if isAnalysiss is tuple else isAnalysiss ,
        self.isAnalysis = self.isAnalysis[0] if isinstance(self.isAnalysis, tuple) else self.isAnalysis

        self.hotelstarAnalysis=hotelstarAnalysis




        # ---
        self.night_count = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
        self.influx = Influxdb()


    def get_data(self):

        try:
            cookies = self.cookies['hotel'][self.target]['cookie']
        except:
            return False


        #---
        if (cookies == {}):
            return False
        #---


        rnd = random.randint(1550000000000000, 1560000000000009)

        headers = {
            'authority': self.cookies['domain'],
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'cache-control': 'max-age=0',
            'origin': f'https://{self.cookies["domain"]}',
            'referer': f'https://{self.cookies["domain"]}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx?action=display&rnd={rnd}',
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
            '__VIEWSTATE': self.cookies['hotel']['view_state'],
            '__VIEWSTATEGENERATOR': self.cookies['hotel']['view_state_generator'],
            '__EVENTVALIDATION': self.cookies['hotel']['event_validation'],
            'dplTo': self.target,
            'dplHotelName': '0',
            'txtCheckinDate': self.start_date_persian,
            'dplNights': self.night_count,
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
            f'https://{self.cookies["domain"]}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        )
        self.influx.capture_logs(1, 'sepehr')

        res = request(
            "GET",
            f"https://{self.cookies['domain']}/systems/FA/Reservation/Hotel_NewReservation_Search.aspx?action=display&rnd={rnd}",
            cookies=cookies,
            verify=False
        )
        self.influx.capture_logs(1, 'sepehr')


        return res.text

    def get_static_data(self):
        with open('/Users/javad/Projects/hotel_providers_api/app_crawl/hotel/test.html', 'r') as html_file:
            data = html_file.read()
            html_file.close()
        return data

    def add_to_file(self, data):
        try:
            file_name = f'{self.provider_name}_{self.start_date.replace("/", "_")}.html'
            path_file = os.path.join(BASE_DIR, 'logs', file_name)
            with open(path_file, 'w', encoding="UTF-8") as html_file:
                html_file.write(data)
                # html_file.close()
            return True
        except:
            return False

    def get_result(self):
        t1=0
        try:
            t1=datetime.now()
            data = self.get_data()
            spendTime = (datetime.now() - t1).total_seconds()
            print(f'{self.provider_name} ---- GetData_{self.start_date} --- {spendTime}')

            t1 = datetime.now()
            soup = BeautifulSoup(data, 'html.parser')
            result = []
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}

        hotels = soup.select("table.Table03:has(tr.header)")


        for hotel in hotels:
            try:

                #---
                hotel_star=hotel.select_one('img[alt*="ستاره"]').get('alt').replace('ستاره','').replace('هتل','').strip()
                hotel_name = hotel.select_one("tr.header td:nth-child(1)").text.strip()
                # ======== Check for hotel names or star ratings
                if self.isAnalysis:
                    # Create a set of all hotel names for faster lookup
                    all_hotel_names = {hotel_name for hotel in hotels}
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
                        hotels = [hotel for hotel in hotels if hotel_name in selected_hotels]
                    else:
                        # Fallback to original star rating and name check
                        hotels = [hotel for hotel in hotels
                                 if (str(hotel['hotel_star']) in self.hotelstarAnalysis)
                                 or (hotel_name in self.hotelstarAnalysis)]

                    if (len(hotels)==0):  # on hotel nashod!
                        continue
                    print('Sepehr Analysis')
                else:
                    print('Sepehr RASII')



                appended_item = {
                    "hotel_name": hotel.select_one("tr.header td:nth-child(1)").text.strip(),
                    "hotel_star": hotel.select_one('img[alt*="ستاره"]').get('alt').replace('ستاره','').replace('هتل','').strip(),
                    "min_price": None,
                    "rooms": [],
                    "provider": self.provider_name
                }
                rooms = hotel.select('.input_hand label')
                room_row = hotel.select("tr[bgcolor='#EEEEEE']:has(.input_hand)")
                for index, room in enumerate(rooms):
                    room_price = ready_price(
                        room_row[index].select_one("td:nth-child(4)").text.strip())
                    try:
                        room_status = room_row[index].select_one("td:nth-child(7)").text.strip()
                        if ('تلفن' in room_status):
                            room_status = "تماس تلفنی"
                            continue
                        #==== Check red color for font
                        try:
                            room_status = room_row[index].select_one("font[color='red']").text.strip()
                            room_status = "تماس تلفنی"
                            continue
                        except:
                            ''
                        #=======


                    except:
                        room_status = "تماس تلفنی"
                        #===========
                        # Skipp tamas telefoni
                        #============
                        continue

                    room_price = convert_to_tooman(room_price)
                    room_item = {
                        "name": room.text.strip(),
                        "capacity": len(room_row[index].select("td:nth-child(5) i")),
                        "price": room_price,
                        "status": room_status,
                        "provider": self.provider_name
                    }
                    # ---
                    if not appended_item['min_price']:
                        appended_item['min_price'] = room_price
                    if room_price < appended_item['min_price']:
                        appended_item['min_price'] = room_price
                    # ---
                    appended_item['rooms'].append(room_item)
                # ---
                appended_item['rooms'] = sorted(appended_item['rooms'], key=lambda k: k['price'], reverse=False)
                result.append(appended_item)
            except:
                print("--------------------------------")
                print(f"{self.provider_name} hotel wrong")

        spendTime = (datetime.now() - t1).total_seconds()
        print(f'{self.provider_name} ---- ParseData_{self.start_date} --- {spendTime}')


        return result

