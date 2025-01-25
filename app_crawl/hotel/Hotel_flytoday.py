import json
from concurrent.futures import ThreadPoolExecutor, wait
from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3
import requests
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import pandas

class FlyToday:
    def __init__(self, target, start_date, end_date, adults):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.headers = {
            'accept': '*/*',
            'accept-language': 'fa-IR',
            'authorization': 'Bearer null',
            'cache-control': 'max-age=0',
            'content-type': 'application/json',
            'origin': 'https://www.flytoday.ir',
            'priority': 'u=1, i',
            'referer': 'https://www.flytoday.ir/',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-app': 'www.flytoday.ir',
            'x-path': 'https://www.flytoday.ir/hotel/search?&regionCode=178267&checkIn=2024-10-23&checkOut=2024-10-27&adt[0]=1&chd[0]=0&chdAges[0]=&dateLang=fa&countryCode=TR',
            # 'x-token': '36366e744c6e7577642b43706e794876357a714141494b39544f3843634f73513677697a2b654a676269714d71506c78475679354c6d61577752697172527636',
        }
        self.static_session_id = ""
        self.cookies = []
        self.countryCode={
            'DXB':'AE',
            'IST':'TR'
        }
        self.regionCode={
            'DXB':'1079',
            'IST':'178267'
        }
    def get_result(self):
        try:

            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            stay_duration = (end_date - start_date).days


            json_data = {
                # 'checkIn': '2024-10-27',
                # 'checkOut': '2024-10-30',

                'checkIn': str(start_date),
                'checkOut': str(end_date),


                'hotelId': None,
                'occupancies': [
                    {
                        'adultCount': 2,
                        'childCount': 0,
                        'childAges': [],
                    },
                ],
                'dateLang': 'fa',
                'NationalityId': 'IR',
                # 'countryCode': 'TR',
                # 'countryCode': 'AE',
                'countryCode':self.countryCode[self.target],
                'cityName': '',
                'hotelName': '',
                'key': '',
                'isJalali': True,
                'isDomestic': False,
                'regionCode': self.regionCode[self.target],  # bayad hatman dorost shavad!!!
            }

            response = requests.post('https://api.flytoday.ir/api/V1/hotel/Availability', headers=self.headers, json=json_data)


            json_data = json.loads(response.text)

            lst_hotels = list()
            hotel_items = json_data['pricedItineraries']
            for item in hotel_items:
                hotel = {}
                hotel['hotel_name'] = item['hotelInfo']['name']
                hotel['hotel_star'] = ''
                hotel['min_price'] = item['totalPrice']
                hotel['provider'] = 'FlyToday'
                hotel['rooms'] = []
                for room in item['rooms']:
                    roomItem = {}
                    roomItem['name'] = room['name']
                    roomItem['price'] = hotel['min_price']
                    roomItem['provider'] = 'FlyToday'
                    hotel['rooms'].append(roomItem)
                lst_hotels.append(hotel)
            # print('asd')
            return lst_hotels

            #
            # if len(lst_hotels) <= 0:
            #     return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
            #
            #
            # return {'status': True, 'data': lst_hotels, 'message': ""}

        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}
