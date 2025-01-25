﻿import json
from datetime import datetime, timedelta
from requests import request
# from app_crawl.helpers import convert_to_tooman
# from app_crawl.cookie.cookie_data import BOOKING as booking_cookie
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Booking:
    def __init__(self,source,target, start_date, night_count, adults=2):
        self.start_date = start_date
        date_obj = datetime.strptime(self.start_date, "%Y-%m-%d")
        next_day = date_obj - timedelta(days=1)
        self.start_date = next_day.strftime("%Y-%m-%d")

        end_date = (datetime.strptime(self.start_date, "%Y-%m-%d").date() + timedelta(days=night_count)).strftime("%Y-%m-%d")



        self.source=source
        self.target=target

        self.night_count = night_count
        self.end_date = end_date
        self.adults = adults
        self.url = f"https://www.booking.ir/trip/?i={self.start_date}&o={self.end_date}&r=1&n=&d=1640809&or=1640810&a={adults}&c=0#/"
        self.cookies = []
        self.header = {
            'Content-Type': 'application/json',
            "Cookie": ""
        }

    # def get_basic_cookies(self):
    #     driver = get_driver()
    #     driver.get(self.url)
    #
    #     self.cookies = [f"{cookie['name']}={cookie['value']}" for cookie in driver.get_cookies()]
    #
    #     driver.close()

    # def get_authorization(self):
    #     self.get_basic_cookies()
    #     url = "https://www.booking.ir/fa/v2/signinbymobile/"
    #
    #     payload = 'mobile=09153148721&password=MST1231020'
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #
    #     req = request("POST", url, headers=headers, data=payload, verify=False)
    #
    #     cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]
    #
    #     self.cookies.extend(cookies)
    #     self.header['Cookie'] = '; '.join(self.cookies)
    #     return req.cookies.get_dict()

    def get_auth(self):
        url = "https://www.booking.ir/fa/v2/signinbymobile/"

        payload = 'mobile=09153148721&password=@MST8451030yf'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req = request("POST", url, headers=headers, data=payload, verify=False)

        cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

        self.cookies.extend(cookies)
        self.header['Cookie'] = '; '.join(self.cookies)
        headers['cookie'] = '; '.join(self.cookies)

        req = request("GET", "https://www.booking.ir/account/getcompanies/", headers=headers, verify=False)

        data = json.loads(req.text)

        company_id = data['model'][0]['id']

        data = F"id={company_id}"

        req = request("POST", "https://www.booking.ir/account/signinbycompany/", headers=headers, data=data)

        print("--------------------------------")
        print(req.text)

        cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

        self.cookies = []
        self.cookies.extend(cookies)
        self.header['cookie'] = '; '.join(self.cookies)

        return req.cookies

    def get_session_id(self):
        self.get_auth()
        req = request("GET", self.url, headers=self.header)

        if req.status_code != 200:
            self.get_session_id()

        req_text = req.text

        basic_index = req_text.find("basic")
        session_index = req_text.find('sessionId')

        session_id = req_text[session_index + 12:basic_index - 3]

        return session_id

    def get_data(self):
        url = f"https://www.booking.ir/trip/searchpackage/?sessionid={self.get_session_id()}"

        req = request("GET", url, headers=self.header)

        if req.status_code != 200:
            self.get_data()

        return json.loads(req.text)

    def get_result(self):
        try:
            #==========ssssssssss
            urll = "http://45.149.76.168:5001/booking_tours"
            params = {
                'start_date': self.start_date,
                'night_count': self.night_count,
                'adults':self.adults,
                'source':self.source,
                'target':self.target

            }
            response = requests.get(urll, params=params)
            data=response.json()

            #=============



            # data = self.get_data()
            if not data['isSucceed']:
                return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}
        # ---
        try:
            go_flight = data['model']['hotelBookingSearchResult']['hotelBookingItineraries'][0]['flightItineraries'][0]['flights'][0]
            go_flight_departure_date = datetime.strptime(go_flight['departureDateTime'], '%Y-%m-%dT%H:%M:%S')
            go_flight = {
                "airline": go_flight['flightsSegments'][0]['airlineTitle'],
                "airline_english": go_flight['flightsSegments'][0]['airlineCode'],
                "flight_number": go_flight['flightsSegments'][0]['flightNumber'],
                "departure_date": go_flight_departure_date.strftime("%Y-%m-%d"),
                "departure_time": go_flight_departure_date.strftime("%H:%M"),
                "arrive_time": go_flight_departure_date.strftime("%H:%M"),
                "price": 0
            }
        except:
            return {'status': False, "data": [], "message": "پرواز رفت یافت نشد"}
        # ---
        try:
            return_flight = data['model']['hotelBookingSearchResult']['hotelBookingItineraries'][0]['flightItineraries'][1]['flights'][0]
            return_flight_departure_date = datetime.strptime(return_flight['departureDateTime'], '%Y-%m-%dT%H:%M:%S')
            return_flight = {
                "airline": return_flight['flightsSegments'][0]['airlineTitle'],
                "airline_english": return_flight['flightsSegments'][0]['airlineCode'],
                "flight_number": return_flight['flightsSegments'][0]['flightNumber'],
                "departure_date": return_flight_departure_date.strftime("%Y-%m-%d"),
                "departure_time": return_flight_departure_date.strftime("%H:%M"),
                "arrive_time": return_flight_departure_date.strftime("%H:%M"),
                "price": 0
            }
        except:
            return {'status': False, 'data': [], 'message': "پرواز برگشت یافت نشد"}
        # ---
        try:
            result = [
                {

                    "hotel_english_name": hotel['hotel']['slug'],
                    "hotel_name": hotel['hotel']['title'],
                    "hotel_star": hotel['hotel']['rating'],
                    "hotel_rooms": [hotel['bestPackage']['packages'][0]['rooms'][0]['roomTypeTitle']],
                    "room_name": hotel['bestPackage']['packages'][0]['rooms'][0]['roomTypeTitle'],
                    "hotel_price": 0,
                    "commission": 0,
                    "status": "تایید شده",
                    "go_flight": go_flight,
                    "return_flight": return_flight,
                    "total_price": int(hotel['bestPackage']['totalPrice']) / 10,
                    "system_provider": "booking",
                    "redirect_link": f"https://www.booking.ir/trip/?i={self.start_date}&o={self.end_date}&r=1&n=&a={self.adults}&c=0#/"
                } for hotel in data['model']['hotelBookingSearchResult']['hotelBookingItineraries']
            ]
            # ---
            return {"status": True, "data": result, 'message': ""}
        except:
            return {'status': False, 'data': [], 'message': "هتل یافت نشد"}


# booking = Booking("2024-08-15", 3,)
# print("--------------------------------")
# print(booking.get_result())
