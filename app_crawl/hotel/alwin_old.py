import json
from requests import request
from app_crawl.helpers import convert_to_tooman
from concurrent.futures import ThreadPoolExecutor


class Alwin24:
    def __init__(self, target, start_date, end_date, adults):
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
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
        url = "https://api.chartex.net/api/v1/auth"

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

    try_again_go=3
    try_again_return=3
    try_hotel=3
    def get_hotels(self):
        try:
            body = json.dumps({
                "IsDynamicTour": True,
                "buyCountryId": "IR",
                "chartexCacheHotelSearchId": 0,
                "isEcotourism": False,
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
            url = "https://api.chartex.net/api2/HotelSearch/search"
            # ---
            req = request("POST", url, headers=self.post_header, data=body)
            # ---
            if req.status_code != 200:
                self.get_hotels()
            # ---
            data = json.loads(req.text)
            dd = data['data']
            if len(dd)==0 and self.try_hotel>=0:
                self.try_hotel=self.try_hotel-1
                self.get_hotels()

            # ---
            return [{
                "hotel_name": hotel['name'],
                "hotel_star": hotel['stars'],
                "min_price": convert_to_tooman(hotel['products_min_price']),
                "rooms": [
                    {
                        "price": convert_to_tooman(room['price']),
                        "name": room['rooms'][0]['hotelRoomTypeName'],
                        "provider": "alwin"
                    } for room in hotel['products']
                ],
                "provider": "alwin"
            } for hotel in data['data']]
        except:
            return []

    def get_result(self):
        try:
            self.get_token()
            return self.get_hotels()
        except:
            return []

# from time import perf_counter
#
#
# start = perf_counter()
#
# alwin = Alwin24("KIH", "2023-02-20", "2023-02-23", 2)
# print("--------------------------------")
# print('allwin', alwin.get_result())
#
# end = perf_counter()
#
# print("--------------------------------")
# print(f"end with ==> {round(end - start, 2)} seconds")
