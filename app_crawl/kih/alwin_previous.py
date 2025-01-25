import json
import time
from datetime import timedelta, datetime

import requests
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
            # "authorization": r"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTk1MTA5NDUsImlhdCI6MTcxOTMzODE0NSwibmJmIjoxNzE5MzM4MTQ1LCJhZCI6MTAyNTk3LCJpZCI6MTAyODczLCJyb2xlIjoiR1VFU1QiLCJzZXNzaW9uX2tleSI6ImxvZ2luX3Nlc3Npb25fMTAyNTk3XzEwMjg3M19taFZYVkR1cTNpeTduUHhraEtqYWJIY3IiLCJwYyI6bnVsbCwiYyI6IklSUiJ9.P1H_Xl_NpKzpwGWXx2H9RsINnDIcH2FFAGLmHczel-0"
        }
        self.executor = ThreadPoolExecutor(max_workers=100)

    def change_time(self, time):
        return f"{time[:2]}:{time[2:]}"

    def get_token(self):

        # #==== without login===
        #
        # self.post_header['authorization']="""JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjAyNTUwNjAsImlhdCI6MTcyMDA4MjI2MCwibmJmIjoxNzIwMDgyMjYwLCJhZCI6MTAyNTk3LCJpZCI6MTAyODczLCJyb2xlIjoiR1VFU1QiLCJzZXNzaW9uX2tleSI6ImxvZ2luX3Nlc3Npb25fMTAyNTk3XzEwMjg3M19BRDFDT1Rjbkp2R1RzaGlubnFCMWZCMHoiLCJwYyI6bnVsbCwiYyI6IklSUiJ9.shDnHCHRUuK4bjid0er1IQc2a9O9yRDajOeZCjUv47I"""
        # return ""
        # #=========
        #
        #
        #
        # """
        # get header token
        # :return: jwt token
        # """
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
        # self.post_header['authorization'] = f"JWT {data['access_token']}"
        return f"JWT {data['access_token']}"
        # return data['access_token']

    def get_go_flight(self,authorization):
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
                "flight_return_date": "",
                "flight_class": "1",
                "origin_trip_type": 1,
                "trip_type": 1,
                "provider_code": "ALLWIN",
                "setMinPerson": True,

                'isTour':True,

            })
            headers = {
                'Content-Type': 'application/json',
                "authorization":authorization
            }

            # ---
            # url = "https://api.chartex.ir/api2/Flights/presearchV3"
            # ---
            # import requests
            # s=requests.session()
            # req = s.post(url=url, headers=self.post_header, data=body)

            url = "https://api.chartex.ir/api2/Flights/searchV3"
            # self.post_header['authorization'] = 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTk2NTE0MzQsImlhdCI6MTcxOTQ3ODYzNCwibmJmIjoxNzE5NDc4NjM0LCJhZCI6MTAyNTk3LCJpZCI6MTAyODczLCJyb2xlIjoiR1VFU1QiLCJzZXNzaW9uX2tleSI6ImxvZ2luX3Nlc3Npb25fMTAyNTk3XzEwMjg3M196RUtjQkJuTHFuMU55czhKYzNkMnNiUlMiLCJwYyI6bnVsbCwiYyI6IklSUiJ9.hdHQPup3Dg9dKE9bl0863YQNK4TjhCgQD6wge6mn-bg'
            # self.get_token()
            req = requests.post(url=url, headers=headers, data=body)

            # ---
            if req.status_code != 200:
                self.get_go_flight()

            data1 = json.loads(req.text)
            data1=data1['data']


            # Twice
            req = requests.post(url=url, headers=headers, data=body)
            if req.status_code != 200:
                self.get_go_flight()

            data2 = json.loads(req.text)
            data2=data2['data']

            if (len(data1)>len(data2)):
                data=data1
            else:
                data=data2

            # ---
            result = []
            # data = json.loads(req.text)
            # data = data['data']
            #======

            if len(data)==0 and self.try_again_go>=0:
                time.sleep(3)
                self.get_token()
                self.try_again_go=self.try_again_go-1
                self.get_go_flight()


            #=====
            for air in data:
                appended_data = {
                    "airline": convert_airlines(air['airline']),
                    # "airline": '',
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

    try_again_go=3
    try_again_return=3
    try_hotel=3
    def get_return_flight(self,authorization):
        try:
            body = json.dumps({
                "adults": self.adults,
                "childs": 0,
                "infant": 0,
                "source": self.destination,
                "destination": self.source,
                "scope": "local",
                "date_string": "",
                "flight_date": f"{self.end_date}",
                "flight_return_date":"",
                # "flight_date": f"{self.end_date}",
                "flight_class": "1",
                "origin_trip_type": 1,
                "trip_type": 1,
                "provider_code": "ALLWIN",
                "setMinPerson": True,

                'isTour': True,
            })
            # body=json.dumps(
            # {"source":"THR",
            #  "destination":"KIH",
            #  "adults":1,
            #  "childs":0,
            #  "infant":0,
            #  "flight_date":"2024-06-26",
            #  "flight_return_date":'',
            #  "flight_class":1,
            #  "origin_trip_type":1,
            #  "provider_code":"ALLWIN",
            #  "scope":"local",
            #  "trip_type":1}
            # )
            headers = {
                'Content-Type': 'application/json',
                "authorization":authorization
            }

            # ---
            #============== Modify OK ========================
            # url = "https://api.chartex.ir/api2/Flights/search"
            url = "https://api.chartex.ir/api2/Flights/searchV3"
            # self.get_token()
            # ---
            # time.sleep(2)
            # self.get_token()

            req = request("POST", url, headers=headers, data=body)
            # ---
            if req.status_code != 200:
                self.get_return_flight()

            data1 = json.loads(req.text)
            data1=data1['data']

            # Twice
            req = request("POST", url, headers=headers, data=body)
            if req.status_code != 200:
                self.get_return_flight()

            data2 = json.loads(req.text)
            data2=data2['data']

            if (len(data1)>len(data2)):
                data=data1
            else:
                data=data2

            # ---
            result = []
            # data = json.loads(req.text)
            # data = data['data']
            #======

            if len(data)==0 and self.try_again_return>=0:
                print(f'Retry Return Flight _ ALWIN__ ... {self.try_again_return}')
                time.sleep(3)
                self.get_token()
                self.try_again_return=self.try_again_return-1
                self.get_return_flight()

            #=====
            for air in data:
                appended_data = {
                    "airline": convert_airlines(air['airline']),
                    # "airline": '',
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

    def get_hotels(self,authorization):
        try:
            body = json.dumps({
                "IsDynamicTour":True,
                "buyCountryId":"IR",
                "chartexCacheHotelSearchId":0,
                "isEcotourism":False,
                "PidIds": None,
                "endDate": f"{self.end_date}T00:00:00.000Z",
                "filters": {},
                "hotelId": 0,
                "hotelTypeId": 1,
                "justChartexHotels": False,
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

            headers = {
                'Content-Type': 'application/json',
                "authorization":authorization
            }

            # ---
            url = "https://api.chartex.net/api2/HotelSearch/search"
            # ---
            # self.get_token()
            req = request("POST", url, headers=headers, data=body)
            # ---
            if req.status_code != 200:
                self.get_hotels()
            # ---
            data = json.loads(req.text)
            dd=data['data']
            if len(dd)==0 and self.try_hotel>=0:
                self.try_hotel=self.try_hotel-1
                self.get_hotels()

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
            go_flight_auth="""JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjAyNTUwNjAsImlhdCI6MTcyMDA4MjI2MCwibmJmIjoxNzIwMDgyMjYwLCJhZCI6MTAyNTk3LCJpZCI6MTAyODczLCJyb2xlIjoiR1VFU1QiLCJzZXNzaW9uX2tleSI6ImxvZ2luX3Nlc3Npb25fMTAyNTk3XzEwMjg3M19BRDFDT1Rjbkp2R1RzaGlubnFCMWZCMHoiLCJwYyI6bnVsbCwiYyI6IklSUiJ9.shDnHCHRUuK4bjid0er1IQc2a9O9yRDajOeZCjUv47I"""
            return_flight_auth="""JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjAyNTczNTAsImlhdCI6MTcyMDA4NDU1MCwibmJmIjoxNzIwMDg0NTUwLCJhZCI6MTAyNTk3LCJpZCI6MTAyODczLCJyb2xlIjoiR1VFU1QiLCJzZXNzaW9uX2tleSI6ImxvZ2luX3Nlc3Npb25fMTAyNTk3XzEwMjg3M18zNTg1UmZiU3NKZUs0Ym5FMkJBV0RuRUEiLCJwYyI6bnVsbCwiYyI6IklSUiJ9.kofKppdnjdzOR36MyPLloWFtFnNj0_edXS6uJvfNrv4"""
            hotel_auth="""JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MjAyNTc0MDYsImlhdCI6MTcyMDA4NDYwNiwibmJmIjoxNzIwMDg0NjA2LCJhZCI6MTAyNTk3LCJpZCI6MTAyODczLCJyb2xlIjoiR1VFU1QiLCJzZXNzaW9uX2tleSI6ImxvZ2luX3Nlc3Npb25fMTAyNTk3XzEwMjg3M19WanRSS1Zma2htSVVjZ2JWUnk0MGc5WksiLCJwYyI6bnVsbCwiYyI6IklSUiJ9.zwB_8e0df11nVZejns5KP1lRra3yamZzyKiIUtQeQEc"""

            # go_flight_auth=self.get_token()
            # return_flight_auth=self.get_token()
            # hotel_auth=self.get_token()


            go_flight = self.executor.submit(self.get_go_flight,go_flight_auth)
            return_flight = self.executor.submit(self.get_return_flight,return_flight_auth)
            hotels = self.executor.submit(self.get_hotels,hotel_auth)

            # ---
            go_flight = go_flight.result()
            return_flight = return_flight.result()
            hotels = hotels.result()


            #=====
            # Check twise
            #=====
            if len(go_flight.keys()) == 0:
                go_flight = self.executor.submit(self.get_go_flight)
                go_flight = go_flight.result()
            if len(return_flight.keys()) == 0:
                return_flight = self.executor.submit(self.get_return_flight)
                return_flight = return_flight.result()
            if len(hotels) == 0:
                hotels = self.executor.submit(self.get_hotels)
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
                    # hotel['total_price'] = ''
                    hotel["system_provider"] = "alwin"
                    hotel["redirect_link"] = "https://allwin24.ir/"
                    result.append(hotel)
            # ---
            return {'status': True, "data": result, 'message': ""}
        except:
            return {"status": False, "data": [], "message": "اتمام زمان"}
#
# from time import perf_counter
# #
# #
# start = perf_counter()
# #
# alwin = Alwin24("2024-07-07", 3)
# print("--------------------------------")
# print(alwin.get_result())
# #
# end = perf_counter()
# #
# print("--------------------------------")
# print(f"end with ==> {round(end - start, 2)} seconds")
