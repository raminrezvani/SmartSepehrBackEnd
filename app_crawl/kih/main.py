from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from operator import itemgetter
from app_crawl.kih.alwin import Alwin24
from app_crawl.kih.booking_api import Booking
from app_crawl.kih.deltaban import Deltaban
from app_crawl.kih.jimbo_api import Jimbo
from app_crawl.ready_tour.sepehr import Sepehr
from app_crawl.cookie import cookie_data
from app_crawl.kih.data import hotels
from app_crawl.helpers import ready_sepehr_hotel_name
from app_crawl.cache.cache import has_key_cache, get_cache, add_cache


class TourCollector:
    def __init__(self, source, target, start_date, night_count, hotel_star, adults=2):
        self.start_date = start_date
        self.source = source
        self.target = target
        try:
            self.end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=int(night_count))
            self.night_count = int(night_count)
        except ValueError:
            self.end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=3)
            self.night_count = night_count
        self.hotel_star = hotel_star
        self.adults = adults
        self.redis_expire = 10 * 60  # 10 minutes
        self.executor = ThreadPoolExecutor(max_workers=200)  # تنظیم تعداد کارگرها
        self.executor_analysis = ThreadPoolExecutor(max_workers=200)




        # تولید یکباره پروایدرها در زمان مقداردهی اولیه
        self.providers_template = [
            ("Booking", lambda s, t, sd, nc, a, i: Booking(s, t, sd, nc, adults=a, iter=i)),
            ("Jimbo", lambda s, t, sd, nc, a, i: Jimbo(s, t, sd, nc, adults=a, iter=i)),
            ("Deltaban", lambda s, t, sd, nc, a, i: Deltaban(sd, nc, s, t, adults=a)),
            ("Dayan", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.DAYAN, "dayan", adults=a)),
            ("Sepid Parvaz", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.SEPID_PARVAZ, "sepid_parvaz", adults=a)),
            ("Mehrab Seir", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.MEHRAB, "mehrab", adults=a)),
            ("Rahbal", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.RAHBAL, "rahbal", adults=a)),
            ("Tak Setare", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.TAK_SETAREH, "tak_setare", adults=a)),
            ("Omid Oj", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.OMID_OJ, "omid_oj", adults=a)),
            ("Parmis", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.PARMIS, "parmis", adults=a)),
            ("HRC", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.HRC, "hrc", adults=a)),
            ("Kimiya", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.TOURISTKISH, "kimiya", adults=a)),
            ("Eram2MHD", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.ERAM2MHD, "eram2mhd", adults=a)),
            ("Safiran", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.SAFIRAN, "safiran", adults=a)),
            ("Hamood", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.HAMOOD, "hamood", adults=a)),
            ("Darvishi", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.DARVISHI, "darvishi", adults=a)),
            ("Moeindarbari", lambda s, t, sd, nc, a, i: Sepehr(s, t, sd, nc, cookie_data.MOEINDARBARI, "moeindarbari", adults=a)),
        ]

    def get_result(self, data):
        sami_result = {}
        for hotel in data:
            appended_data = {
                "hotel_name": hotel['hotel_name'],
                "system_provider": hotel['system_provider'],
                "room_name": hotel['room_name'],
                "total_price": float(hotel['total_price']) - (float(hotel['commission']) * self.adults),
                "commission": hotel['commission'],
                "status": ready_sepehr_hotel_name(hotel['status']),
                "go_flight_price": hotel['go_flight']['price'],
                "go_flight_airline": hotel['go_flight']['airline'],
                "go_flight_arrive_time": hotel['go_flight']['arrive_time'],
                "return_flight_price": hotel['return_flight']['price'],
                "return_flight_airline": hotel['return_flight']['airline'],
                "return_flight_arrive_time": hotel['return_flight']['arrive_time'],
                "redirect_link": hotel['redirect_link'],
                "hotel_star": 3
            }

            if self.target == "KIH":
                for key, value in hotels.items():
                    system_provider = value[hotel['system_provider']]
                    if system_provider:
                        if hotel['system_provider'] == "alibaba":
                            hotel_name = hotel['hotel_name']
                            if system_provider == hotel_name:
                                appended_data['hotel_name'] = key
                                appended_data['hotel_star'] = value['hotel_star']
                                break
                        else:
                            hotel_name = ready_sepehr_hotel_name(hotel['hotel_name'])
                            if system_provider.strip() in hotel_name:
                                appended_data['hotel_name'] = key
                                appended_data['hotel_star'] = value['hotel_star']

            hotel_name = appended_data['hotel_name']
            if hotel_name in sami_result:
                instance = sami_result[hotel_name]
                if int(appended_data['total_price']) < int(instance['price']):
                    instance['price'] = appended_data['total_price']
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
                    "providers": [{
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
                    }]
                }

        result = [provider for provider in sami_result.values()]
        for provider in result:
            provider['providers'] = sorted(provider['providers'], key=itemgetter('price'))
        return result

    def get_single_data(self, source, target, start_date, use_cache, iter):
        print(f"Processing data for date: {start_date}")
        print("-" * 40)

        # تولید پروایدرها با استفاده از قالب تعریف‌شده
        providers = [(name, factory(source, target, start_date, self.night_count, self.adults, iter))
                     for name, factory in self.providers_template]

        tasks = {self.executor.submit(instance.get_result): name for name, instance in providers}
        results = []
        provider_status = {}
        start_time = datetime.now()

        for future in as_completed(tasks):
            name = tasks[future]
            try:
                result = future.result()
                results.extend(result.get('data', []))
                spend_time = (datetime.now() - start_time).total_seconds()
                print(f'{name} -----> spend: {spend_time}')
                provider_status[name] = {"length": len(result.get('data', [])), "message": result.get('message', '')}
            except Exception as e:
                print(f"{name} failed: {str(e)}")
                provider_status[name] = {"length": 0, "message": "Timeout/Error"}

        for provider, status in provider_status.items():
            print(f"{provider}: {status}")

        return {'data': results, "providers": provider_status}

    def get_single_result(self, source, target, start_date=None, show_providers=False, use_cache=True, iter=1):
        start_date = start_date or self.start_date
        redis_key = f"ready_{source}_{target}_{start_date}_{self.night_count}_{self.adults}"

        if use_cache and has_key_cache(key=redis_key):
            print('get from cache')
            data = get_cache(key=redis_key, get_time=True)
            return data if show_providers else data['data']

        data = self.get_single_data(source, target, start_date, use_cache, iter)
        result = self.get_result(data['data'])

        if result:
            # add_cache(redis_key,{'data': result, 'providers': data['providers']})
            # print('Start caching...')
            with ThreadPoolExecutor(max_workers=1) as executor_cache:
                executor_cache.submit(add_cache, redis_key, {'data': result, 'providers': data['providers']})










        return {'data': result, 'providers': data['providers']} if show_providers else result

    def get_analysis(self, source, target, range_number: int, use_cache=True):
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        date_range = [(start_date + timedelta(days=date)).strftime("%Y-%m-%d") for date in range(range_number)]

        futures = {self.executor_analysis.submit(self.get_single_result, source, target, date, False, use_cache, iter): date
                   for iter, date in enumerate(date_range)}

        result = {}
        start_time = datetime.now()

        for future in as_completed(futures):
            date = futures[future]
            try:
                res = future.result()
                print(f'Future completed in {(datetime.now() - start_time).total_seconds()}')
                result[date] = res
            except Exception as e:
                print(f"An error occurred: {e}")

        sorted_result = {date: result[date] for date in sorted(result.keys())}
        return {'status': True, "data": sorted_result}

    def __del__(self):
        # آزادسازی منابع ThreadPoolExecutor
        self.executor.shutdown(wait=False)
        self.executor_analysis.shutdown(wait=False)