import json
from datetime import datetime
from app_crawl.helpers import convert_to_tooman, convert_gregorian_date_to_persian

from requests import request
from concurrent.futures import ThreadPoolExecutor


class Alibaba:
    def __init__(self, start_date, end_date, source, target):
        self.start_date = start_date
        self.end_date = end_date
        self.source = source
        self.target = target
        self.executor = ThreadPoolExecutor(max_workers=5)

    def get_token(self, go: bool = True):
        req_url = "https://ws.alibaba.ir/api/v1/flights/domestic/available"

        req_body = {
            "origin": self.source,
            "destination": self.target,
            "departureDate": self.start_date if go else self.end_date,
            "adult": 1,
            "child": 0,
            "infant": 0
        }

        req_header = {
            'Content-Type': 'application/json',
        }

        req = request("POST", req_url, headers=req_header, json=req_body)

        data = json.loads(req.text)

        return data['result']['requestId']

    def get_go_flight(self):
        token = self.get_token()

        req_url = f"https://ws.alibaba.ir/api/v1/flights/domestic/available/{token}"

        req = request("GET", req_url)

        result = []
        if req.status_code == 200:
            data = json.loads(req.text)['result']['departing']

            result = [
                {
                    "airline_name": flight['airlineName'],
                    "airline_code": flight['airlineCode'],
                    "go_time": datetime.strptime(flight['leaveDateTime'], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M"),
                    "go_date": convert_gregorian_date_to_persian(self.start_date)['date'],
                    "return_time": convert_gregorian_date_to_persian(
                        datetime.strptime(flight['arrivalDateTime'], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M"))['date'],
                    "return_date": convert_gregorian_date_to_persian(
                        datetime.strptime(flight['arrivalDateTime'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))['date'],
                    "flight_number": flight['flightNumber'],
                    "provider_name": "علی بابا",
                    "provider_logo": f"https://cdn.alibaba.ir/h2/desktop/apple-touch-icon.png",
                    "price": convert_to_tooman(flight['priceAdult']),
                    "seat": flight['seat'],
                    "buy_link": f'https://www.alibaba.ir/'
                } for flight in data
            ]

            return result
        else:
            return result

    def get_return_flight(self):
        token = self.get_token(False)

        req_url = f"https://ws.alibaba.ir/api/v1/flights/domestic/available/{token}"

        req = request("GET", req_url)

        result = []
        if req.status_code == 200:
            data = json.loads(req.text)['result']['departing']

            result = [
                {
                    "airline_name": flight['airlineName'],
                    "airline_code": flight['airlineCode'],
                    "go_time": datetime.strptime(flight['leaveDateTime'], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M"),
                    "go_date": convert_gregorian_date_to_persian(self.end_date)['date'],
                    "return_time": convert_gregorian_date_to_persian(
                        datetime.strptime(flight['arrivalDateTime'], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M"))['date'],
                    "return_date": convert_gregorian_date_to_persian(
                        datetime.strptime(flight['arrivalDateTime'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))['date'],
                    "flight_number": flight['flightNumber'],
                    "provider_name": "علی بابا",
                    "provider_logo": f"https://cdn.alibaba.ir/h2/desktop/apple-touch-icon.png",
                    "price": convert_to_tooman(flight['priceAdult']),
                    "seat": flight['seat'],
                    "buy_link": f'https://www.alibaba.ir/'
                } for flight in data
            ]

            return result
        else:
            return result

    def get_result(self, one_way=True):
        try:
            result = dict()
            go_flight = self.executor.submit(self.get_go_flight)
            if not one_way:
                return_flight = self.executor.submit(self.get_return_flight)
                result['go_flight'] = go_flight.result()
                result['return_flight'] = return_flight.result()
            else:
                result = go_flight.result()
            # ---
            return result
        except:
            return {"go_flight": [], "return_flight": []} if not one_way else []

# alibaba = Alibaba("2023-01-30", "2023-02-02", "MHD", "THR")
# print("--------------------------------")
# print(alibaba.get_result(False))
