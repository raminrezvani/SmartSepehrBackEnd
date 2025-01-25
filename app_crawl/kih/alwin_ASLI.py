import json
from datetime import timedelta, datetime
from requests import request
from app_crawl.helpers import convert_to_tooman, convert_airlines
from concurrent.futures import ThreadPoolExecutor


class Alwin24:
    def __init__(self, start_date, night_count, target="KIH", adults=2):
        end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=night_count)
        self.start_date = start_date
        self.night_count = night_count
        self.end_date = end_date.strftime("%Y-%m-%d")
        self.adults = adults
        if target == "MHD":
            self.source = "THR"
            self.destination = target
        else:
            self.source = "MHD"
            self.destination = target
        self.post_header = {
            'Content-Type': 'application/json',
            "authorization": ""
        }
        self.executor = ThreadPoolExecutor(max_workers=100)

    def change_time(self, time):
        return f"{time[:2]}:{time[2:]}"

    def get_token(self):
        """
        get header token
        :return: jwt token
        """
        url = "https://api.chartex.ir/api/v1/auth"

        payload = json.dumps({
            "username": "9150028721",
            "password": "@MST8451030yf"
        })

        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            "provider-code": "ALLWIN"
        }

        req = request("POST", url, data=payload, headers=header)
        # ---
        if req.status_code != 200:
            self.get_token()
        # ---
        data = json.loads(req.text)
        self.post_header['authorization'] = f"JWT {data['access_token']}"
        return data['access_token']

    def get_go_flight(self):
        try:
            body = json.dumps({
                "adults": self.adults,
                "childs": 0,
                "infant": 0,
                "source": self.source,
                "destination": self.destination,
                "scope": "local",
                "date_string": "",
                "flight_date": f"{self.start_date}T00:00:00.000Z",
                "flight_class": "1",
                "origin_trip_type": 1,
                "trip_type": 1,
                "provider_code": "ALLWIN",
                "setMinPerson": True
            })
            # ---
            url = "https://api.chartex.ir/api2/Flights/searchV3"
            # ---
            self.get_token()
            req = request("POST", url, headers=self.post_header, data=body)
            # ---
            if req.status_code != 200:
                self.get_go_flight()
            # ---
            result = []
            data = json.loads(req.text)
            data=data['data']
            for air in data:
                appended_data = {
                    "airline": convert_airlines(air['airline']),
                    "arrive_time": self.change_time(air['departs']),
                    "price": min([flight['fee'] for flight in air['classes']])
                }
                result.append(appended_data)
            # ---
            result = list(sorted(result, key=lambda item: item['price']))
            # ---
            return result[0]
        except:
            return {}

    def get_return_flight(self):
        try:
            body = json.dumps({
                "adults": self.adults,
                "childs": 0,
                "infant": 0,
                "source": self.destination,
                "destination": self.source,
                "scope": "local",
                "date_string": "",
                "flight_date": f"{self.end_date}T00:00:00.000Z",
                "flight_class": "1",
                "origin_trip_type": 2,
                "trip_type": 1,
                "provider_code": "ALLWIN",
                "setMinPerson": True
            })
            # ---
            url = "https://api.chartex.ir/api2/Flights/searchV3"
            # ---
            self.get_token()
            req = request("POST", url, headers=self.post_header, data=body)
            # ---
            if req.status_code != 200:
                self.get_go_flight()
            # ---
            result = []
            data = json.loads(req.text)
            data=data['data']
            for air in data:
                appended_data = {
                    "airline": convert_airlines(air['airline']),
                    "arrive_time": self.change_time(air['departs']),
                    "price": min([flight['fee'] for flight in air['classes']])
                }
                result.append(appended_data)
            # ---
            result = list(sorted(result, key=lambda item: item['price']))[0]
            # ---
            return result
        except:
            return {}

    def get_hotels(self):
        try:
            body = json.dumps({
                "PidIds": None,
                "endDate": f"{self.end_date}T00:00:00.000Z",
                "filters": {},
                "hotelId": 0,
                "hotelTypeId": 1,
                "justChartexHotels": None,
                "lang": "fa",
                "limit": 150,
                "locationId": 0,
                "iataCode": self.destination,
                "passengerCounts": [
                    {
                        "roomId": 0,
                        "adultCount": self.adults,
                        "childAge": []
                    }
                ],
                "skip": 0,
                "sortValue": [
                    {
                        "propertyName": "price",
                        "isASC": True
                    }
                ],
                "startDate": f"{self.start_date}T00:00:00.000Z",
                "showHotelAgentService": True,
                "reserveTypeId": 1
            })
            # ---
            url = "https://api.chartex.ir/api2/HotelSearch/search"
            # ---
            req = request("POST", url, headers=self.post_header, data=body)
            # ---
            if req.status_code != 200:
                self.get_hotels()
            # ---
            data = json.loads(req.text)
            # ---
            return [
                {
                    "hotel_name": hotel['name'],
                    "room_name": hotel['products'][0]['rooms'][0]['hotelRoomTypeName'],
                    "room_price": hotel['products_min_price']
                } for hotel in data['data']
            ]
        except:
            return []

    def get_result(self):
        try:
            self.get_token()
            go_flight = self.executor.submit(self.get_go_flight)
            return_flight = self.executor.submit(self.get_return_flight)
            hotels = self.executor.submit(self.get_hotels)
            # ---
            go_flight = go_flight.result()
            return_flight = return_flight.result()
            hotels = hotels.result()
            if len(go_flight.keys()) == 0:
                return {"status": False, "data": [], "message": "پرواز رفت یافت نشد"}
            if len(return_flight.keys()) == 0:
                return {"status": False, "data": [], "message": "پرواز برگشت یافت نشد"}
            if len(hotels) == 0:
                return {"status": False, "data": [], "message": "هتل یافت نشد"}
            # ---
            result = []
            for hotel in hotels:
                if hotel['room_price']:
                    hotel['go_flight'] = go_flight
                    hotel['return_flight'] = return_flight
                    price = round(hotel['room_price'] / self.adults, 2) + hotel['go_flight']['price'] + hotel['return_flight'][
                        'price']
                    hotel["commission"] = 0
                    hotel["status"] = "تایید شده"
                    hotel['per_person'] = price
                    hotel['total_price'] = convert_to_tooman(hotel['per_person'] * self.adults)
                    hotel["system_provider"] = "alwin"
                    hotel["redirect_link"] = "https://allwin24.ir/"
                    result.append(hotel)
            # ---
            return {'status': True, "data": result, 'message': ""}
        except:
            return {"status": False, "data": [], "message": "اتمام زمان"}

# from time import perf_counter
#
#
# start = perf_counter()
#
# alwin = Alwin24("2023-01-29", 3)
# print("--------------------------------")
# print(alwin.get_result())
#
# end = perf_counter()
#
# print("--------------------------------")
# print(f"end with ==> {round(end - start, 2)} seconds")
