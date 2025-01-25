from datetime import datetime, timedelta
from app_crawl.ready_tour.sepehr import Sepehr
from app_crawl.cookie import cookie_data
from app_crawl.gsm.data import hotels_GSM
from app_crawl.kih.alwin import Alwin24
from app_crawl.kih.deltaban import Deltaban
from app_crawl.helpers import (ready_sepehr_gsm_hotel_name, )
from operator import itemgetter
from concurrent.futures import ThreadPoolExecutor


class TourCollector:
    def __init__(self, start_date, night_count, hotel_star):
        self.start_date = start_date
        try:
            self.end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=int(night_count))
            self.night_count = int(night_count)
        except:
            self.end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=3)
            self.night_count = night_count
        self.hotel_star = hotel_star
        self.executor = ThreadPoolExecutor(max_workers=100)

    @staticmethod
    def get_result(data):
        sami_result = {}
        for hotel in data:
            appended_data = {
                "hotel_name": ready_sepehr_gsm_hotel_name(hotel['hotel_name']),
                "system_provider": hotel['system_provider'],
                "room_name": hotel['room_name'],
                "total_price": float(hotel['total_price']) - (float(hotel['commission']) * 2),
                "commission": hotel['commission'],
                "status": hotel['status'],
                "go_flight_price": hotel['go_flight']['price'],
                "go_flight_airline": hotel['go_flight']['airline'],
                "go_flight_arrive_time": hotel['go_flight']['arrive_time'],
                "return_flight_price": hotel['return_flight']['price'],
                "return_flight_airline": hotel['return_flight']['airline'],
                "return_flight_arrive_time": hotel['return_flight']['arrive_time'],
                "redirect_link": hotel['redirect_link'],
                "hotel_star": 3
            }
            # ---
            for key, value in hotels.items():
                system_provider = value[hotel['system_provider']]
                if system_provider:
                    hotel_name = ready_sepehr_gsm_hotel_name(hotel['hotel_name'])
                    if system_provider.strip() in hotel_name:
                        appended_data['hotel_name'] = key
                        appended_data['hotel_star'] = value['hotel_star']
            # ---
            hotel_name = appended_data['hotel_name']
            if hotel_name in list(sami_result.keys()):
                instance = sami_result[hotel_name]
                if int(appended_data['total_price']) < int(instance['price']):
                    instance['price'] = appended_data['total_price']
                # ---
                instance['providers'].append({
                    "room_name": appended_data['room_name'],
                    "provider_name": appended_data['system_provider'],
                    "go_flight_price": appended_data['go_flight_price'],
                    "go_flight_airline": appended_data['go_flight_airline'],
                    "go_flight_arrive_time": appended_data['go_flight_arrive_time'],
                    "return_flight_price": appended_data['return_flight_price'],
                    "return_flight_airline": appended_data['return_flight_airline'],
                    "return_flight_arrive_time": appended_data['return_flight_arrive_time'],
                    "price": appended_data['total_price'],
                    "status": appended_data['status'],
                    "commission": appended_data['commission'],
                    "redirect_link": appended_data['redirect_link'],
                })
            else:
                sami_result[hotel_name] = {
                    "hotel_name": hotel_name,
                    "hotel_star": appended_data['hotel_star'],
                    "price": appended_data['total_price'],
                    "providers": [
                        {
                            "room_name": appended_data['room_name'],
                            "provider_name": appended_data['system_provider'],
                            "go_flight_price": appended_data['go_flight_price'],
                            "go_flight_airline": appended_data['go_flight_airline'],
                            "go_flight_arrive_time": appended_data['go_flight_arrive_time'],
                            "return_flight_price": appended_data['return_flight_price'],
                            "return_flight_airline": appended_data['return_flight_airline'],
                            "return_flight_arrive_time": appended_data['return_flight_arrive_time'],
                            "price": appended_data['total_price'],
                            "redirect_link": appended_data['redirect_link'],
                            "status": appended_data['status'],
                            "commission": appended_data['commission'],
                        }
                    ]
                }

        sami_result = list(sami_result.values())
        result = []
        for provider in sami_result:
            provider['providers'] = sorted(provider['providers'], key=itemgetter('price'), reverse=False)
            result.append(provider)
        # ---
        return result

    def get_single_data(self, start_date):
        # ---
        result = []
        print("--------------------------------")
        print(start_date)
        print("--------------------------------")
        print("deltaban start")
        deltaban_instance = Deltaban(start_date, self.night_count, "GSM")
        deltaban = self.executor.submit(deltaban_instance.get_result)
        print("--------------------------------")
        print("alwin start")
        alwin_instance = Alwin24(start_date, self.night_count, "GSM")
        alwin = self.executor.submit(alwin_instance.get_result)
        print("--------------------------------")
        print("dayan start")
        dayan_instance = Sepehr("GSM", start_date, self.night_count, cookie_data.DAYAN, "dayan")
        dayan = self.executor.submit(dayan_instance.get_result)
        print("--------------------------------")
        print("rahbal start")
        rahbal_instance = Sepehr("GSM", start_date, self.night_count, cookie_data.RAHBAL, "rahbal")
        rahbal = self.executor.submit(rahbal_instance.get_result)
        # ---
        try:
            alwin = alwin.result(timeout=100)
        except TimeoutError:
            print("--------------------------------")
            print("alwin time out")
            alwin = {'status': False, 'data': [], 'message': "خطای سیستم"}
        # ---
        try:
            deltaban = deltaban.result(timeout=100)
        except TimeoutError:
            print("--------------------------------")
            print("deltaban time out")
            deltaban = {'status': False, 'data': [], 'message': "خطای سیستم"}
        # ---
        try:
            dayan = dayan.result(timeout=100)
        except TimeoutError:
            print("--------------------------------")
            print("dayan time out")
            dayan = {'status': False, 'data': [], 'message': "خطای سیستم"}
        # ---
        try:
            rahbal = rahbal.result(timeout=100)
        except TimeoutError:
            print("--------------------------------")
            print("rahbal time out")
            rahbal = {'status': False, 'data': [], 'message': "خطای سیستم"}
        # ---
        providers = {}
        # ---
        if isinstance(alwin, dict):
            result.extend(alwin['data'])
            providers['alwin'] = {
                "length": len(alwin['data']),
                "message": alwin['message']
            }
        # ---
        if isinstance(deltaban, dict):
            result.extend(deltaban['data'])
            providers['deltaban'] = {
                "length": len(deltaban['data']),
                "message": deltaban['message']
            }
        # ---
        if isinstance(dayan, dict):
            result.extend(dayan['data'])
            providers['dayan'] = {
                "length": len(dayan['data']),
                "message": dayan['message']
            }
        # ---
        if isinstance(rahbal, dict):
            result.extend(rahbal['data'])
            providers['rahbal'] = {
                "length": len(rahbal['data']),
                "message": rahbal['message']
            }
        # ---
        print(f"{start_date} done => {providers}")
        return {'data': result, "providers": providers}

    def get_single_result(self, start_date=None, show_providers=False):
        if start_date:
            start_date = start_date
        else:
            start_date = self.start_date
        # ---
        data = self.get_single_data(start_date)
        result = self.get_result(data['data'])
        # ---
        if show_providers:
            return {'data': result, 'providers': data['providers']}
        else:
            return result

    def get_analysis(self, range_number: int):
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        date_range = [(start_date + timedelta(days=date)).strftime("%Y-%m-%d") for date in range(range_number)]
        # ---
        sami_result = self.executor.map(self.get_single_result, date_range)
        result = {date_range[index]: r for index, r in enumerate(sami_result)}
        return {'status': True, "data": result}


# gsm = TourCollector("2023-04-15", 3, 3)
# print("--------------------------------")
# print(gsm.get_single_result(show_providers=True))
