import json
from concurrent.futures import ThreadPoolExecutor, wait
from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Booking:
    def __init__(self, target, start_date, end_date, adults):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.url = f"https://www.booking.ir/fa/hotel/iran/{target.lower()}/?i={self.start_date}&o={self.end_date}&r=1;&n=ir&d=1640809&lt=1&dt=2&a=2&c=0#/"
        self.header = {
            'Content-Type': 'application/json'
        }
        self.login = {
            "username": "09150028721",  # default => deltaban_guest
            "password": "09153787819"  # default => guest
        }
        self.static_session_id = ""
        self.cookies = []

    def get_auth(self):
        url = "https://www.booking.ir/fa/v2/signinbymobile/"

        payload = 'mobile=09153148721&password=MST1231020'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req = request("POST", url, headers=headers, data=payload, verify=False)

        cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

        self.cookies.extend(cookies)
        self.header['Cookie'] = '; '.join(self.cookies)

        req = request("GET", "https://www.booking.ir/account/getcompanies/", headers=headers, verify=False)

        data = json.loads(req.text)

        company_id = data['model'][0]['id']

        data = F"id={company_id}"

        req = request("POST", "https://www.booking.ir/account/signinbycompany/", headers=headers, data=data)

        cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

        self.cookies.extend(cookies)
        self.header['Cookie'] = '; '.join(self.cookies)

        return req.cookies

    def get_session_id(self):
        # self.get_authorization()
        req = request("GET", self.url, headers=self.header)

        if req.status_code != 200:
            self.get_session_id()

        req_text = req.text

        basic_index = req_text.find("destinations")
        session_index = req_text.find('sessionId')

        session_id = req_text[session_index + 12:basic_index - 3]

        self.static_session_id = session_id
        return session_id

    def get_data(self):
        self.get_session_id()
        url = f"https://www.booking.ir/v3/hotelbooking/search/"

        body = {
            "isStaticPage": False,
            "checkIn": f"{self.start_date}T00:00:00",
            "checkOut": f"{self.end_date}T00:00:00",
            "systemType": None,
            "room": 1,
            "nationality": "IR",
            "sessionId": self.static_session_id,
            "destinations": {
                "id": "1640809"
            },
            "occupancies": [
                {
                    "adult": self.adults,
                    "childs": 0,
                    "ages": []
                }
            ]
        }

        req = request("POST", url, json=body, headers=self.header)

        if req.status_code != 200:
            self.get_data()

        return json.loads(req.text)

    def get_room_data(self, data):
        url = f'https://www.booking.ir/v3/hotelbooking/search/'
        print("--------------------------------------")
        print("room run")

        body = {
            "isStaticPage": False,
            "checkIn": f"{self.start_date}T00:00:00",
            "checkOut": f"{self.end_date}T00:00:00",
            "systemType": None,
            "room": 1,
            "nationality": "IR",
            "sessionId": self.static_session_id,
            "destinations": {
                "id": data['hotelId']
            },
            "occupancies": [
                {
                    "adult": self.adults,
                    "childs": 0,
                    "ages": []
                }
            ]
        }

        req = request("POST", url, json=body, headers=self.header)

        if req.status_code == 200:
            data = json.loads(req.text)

            return [
                {
                    "price": convert_to_tooman(room['totalPrice']),
                    "name": room['rooms'][0]['roomTypeTitle'],
                    "provider": "booking",
                    "buy_link": "https://booking.ir/"
                }
                for room in data['model']['hotelBookingItineraries'][0]['packages']
            ]

        else:
            return None

    def get_result(self):
        try:
            data = self.get_data()
            if not data['isSucceed']:
                return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}
        hotels = data['model']['hotelBookingItineraries']
        result = []

        def hotel_handler(hotel):
            result.append({
                "hotel_name": hotel['hotel']['title'],
                "hotel_star": hotel['hotel']['rating'],
                "min_price": convert_to_tooman(hotel['bestPackage']['totalPrice']),
                "rooms": self.get_room_data(hotel)
            })

        # self.executor.map(hotel_handler, hotels)
        future = [self.executor.submit(hotel_handler, hotel) for hotel in hotels]

        wait(future)

        return result
