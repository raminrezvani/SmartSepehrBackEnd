import json
from concurrent.futures import ThreadPoolExecutor
from datetime import (datetime, timedelta)

from requests import request

from app_crawl.kih.data import hotels
from app_crawl.helpers import (convert_gregorian_date_to_persian, convert_to_tooman)


class Alibaba:
    def __init__(self, start_date, night_count):
        end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=night_count)
        self.start_date = start_date
        self.night_count = night_count
        self.end_date = end_date.strftime("%Y-%m-%d")
        self.source = "MHD"
        self.destination = "KIH"

    def correct_time(self, time):
        return time[11:-3]

    def correct_date(self, date):
        date = date[:10]
        return convert_gregorian_date_to_persian(date)['date']

    def get_data(self, key):
        try:
            url = f"https://ws.alibaba.ir/api/v2/tour/available-api/available/pdp-result?origin=iran-mashhad&destination=iran-kish_island&rooms=2&from={self.start_date}&to={self.end_date}&key={key}&page=1"
            # ---
            req = request("GET", url)
            # ---
            result = []
            available_room = []
            if req.status_code == 200:
                data = json.loads(req.text)
                if data['success']:
                    for __room in data['result']['pdpItems']:
                        for _room in __room['saleOptions']:
                            # --- check capacity
                            if _room['adults'] != 2:
                                continue
                            # ---
                            go_flight = {
                                "airline": _room['transports'][0]['transportLine'],
                                "airline_english": _room['transports'][0]['transportLineCode'],
                                "flight_number": _room['transports'][0]['transportNo'],
                                "departure_date": self.correct_date(_room['transports'][0]['arrivalTime']),
                                "departure_time": self.correct_time(_room['transports'][0]['arrivalTime']),
                                "arrive_date": self.correct_date(_room['transports'][0]['departureTime']),
                                "arrive_time": self.correct_time(_room['transports'][0]['departureTime']),
                                "agency": _room['transports'][0]['transportLine'],
                                "price": None
                            }
                            # ---
                            return_flight = {
                                "airline": _room['transports'][1]['transportLine'],
                                "airline_english": _room['transports'][1]['transportLineCode'],
                                "flight_number": _room['transports'][1]['transportNo'],
                                "departure_date": self.correct_date(_room['transports'][1]['arrivalTime']),
                                "departure_time": self.correct_time(_room['transports'][1]['arrivalTime']),
                                "arrive_date": self.correct_date(_room['transports'][1]['departureTime']),
                                "arrive_time": self.correct_time(_room['transports'][1]['departureTime']),
                                "agency": _room['transports'][1]['transportLine'],
                                "price": None
                            }
                            # ---
                            for room in _room['accommodations']:
                                room_name = room['accommodationInfos'][0]['name']
                                if room_name not in available_room:
                                    result.append({
                                        "hotel_name": key,
                                        "hotel_name_eng": room['accommodationInfos'][0]['hotel'],
                                        "room_name": room_name,
                                        "room_price": "",
                                        "commission": 0,
                                        "status": "تایید شده",
                                        "go_flight": go_flight,
                                        "return_flight": return_flight,
                                        "per_person": convert_to_tooman(_room['personPrice']),
                                        "total_price": convert_to_tooman(_room['totalPrice']),
                                        "system_provider": "alibaba",
                                        "redirect_link": f"https://www.alibaba.ir/tour/iran-mashhad/iran-kish_island/{key}?from={self.start_date}&to={self.end_date}&rooms=2"
                                    })
                                    available_room.append(room_name)
            # ---
            return result
        except:
            return []

    def get_result(self):
        try:
            hotel_keys = [value['alibaba'] for key, value in hotels.items() if value['alibaba']]
            executor = ThreadPoolExecutor(max_workers=100)

            def thread_func(key):
                return self.get_data(key)

            result = []
            thread_result = executor.map(thread_func, hotel_keys)
            for r in thread_result:
                result.extend(r)
            # ---
            return {'status': True, "data": result, "message": ""}
        except:
            return {'status': False, "data": [], "message": "مشکلی پیش آمده است"}


# alibaba = Alibaba("2023-01-28", 3)
# print("--------------------------------")
# print(alibaba.get_result())
