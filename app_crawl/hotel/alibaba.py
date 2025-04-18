import json
from concurrent.futures import ThreadPoolExecutor

from requests import request


class Alibaba:
    def __init__(self, target, start_date, end_date, adults):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.executor = ThreadPoolExecutor(max_workers=50)

    def get_target_id(self):
        cities = {
            "KIH": "5be3f68be9a116befc66704b",
            "THR": "5be3f68be9a116befc6669e7"
        }
        return cities.get(self.target, "5be3f68be9a116befc66704b")

    def get_token(self):
        req_url = "https://ws.alibaba.ir/api/v1/hotel/search"

        req_body = {
            "checkIn": self.start_date,
            "checkOut": self.end_date,
            "destination": {
                "type": "City",
                "id": self.get_target_id()
            },
            "rooms": [
                {
                    "adults": [30 for _ in range(self.adults)],
                    "children": []
                }
            ]
        }

        req = request("POST", req_url, json=req_body)

        data = json.loads(req.text)

        return data['result']['sessionId']

    def get_hotels(self):
        req_url = "https://ws.alibaba.ir/api/v1/hotel/result"

        result = []
        skip_count = 0
        token = self.get_token()
        req_body = {
            "sessionId": token,
            "filter": [],
            "sort": {
                "order": -1,
                "field": "score"
            },
            "skip": skip_count,
            "limit": 20
        }

        req = request("POST", req_url, json=req_body)

        data = json.loads(req.text)['result']

        if len(data['result']):
            result.extend([hotel['link'] for hotel in data['result']])
            skip_count += 20
        # ---
        return {'hotels': result, "session_id": token}

    def get_data(self):
        data = self.get_hotels()

        result = []

        # ---
        def get_room(hotel_link):
            req_url = f"https://ws.alibaba.ir/api/v1/hotel/id/{hotel_link}"

            req = request("GET", req_url)

            hotel_id = json.loads(req.text)['result']['id']

            req_url = "https://ws.alibaba.ir/api/v1/hotel/rate/room"

            req_body = {
                "hotelId": hotel_id,
                "sessionId": data['session_id']
            }

            req = request("POST", req_url, json=req_body)

            room_data = json.loads(req.text)

            print("--------------------------------")
            print(req_body, hotel_link)
            print(room_data['result']['rooms'])

        # ---
        self.executor.map(get_room, data['hotels'])
        # ---
        return result