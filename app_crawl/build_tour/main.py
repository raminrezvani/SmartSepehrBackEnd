import json
import traceback
from app_crawl.hotel.main import Hotel
from app_crawl.flight.main import Flight
from app_crawl.cache.cache import add_cache, get_cache, has_key_cache

from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime, timedelta
import traceback
from collections import defaultdict
import logging
logger = logging.getLogger('django')
# from monitoring import influx_grafana
class BuildTour:
    def __init__(self, source, target, start_date, end_date, adults,priorityTimestamp):
        self.source = source
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults

        self.priorityTimestamp=priorityTimestamp
    def get_flight(self):
        flight = Flight(start_date=self.start_date, end_date=self.end_date, source=self.source, target=self.target,
                        one_way=False)
        return flight.get_result()

    def get_hotel(self,use_cache,iter):
        hotel = Hotel(source=self.source, target=self.target, start_date=self.start_date, end_date=self.end_date,
                      adults=self.adults,use_cache=use_cache,isAnalysiss=False,hotelstarAnalysis=[],priorityTimestamp=self.priorityTimestamp)
        return hotel.get_result(iter)

    from concurrent.futures import ThreadPoolExecutor, TimeoutError
    import traceback

    def get_result(self, use_cache=True, iter=1):
        try:
            redis_key = f"build_tour_{self.source}_{self.target}_{self.start_date}_{self.end_date}"

            # Check cache before execution
            if use_cache and has_key_cache(redis_key):
                return get_cache(redis_key)

            # --- consider also Pending caches ---
            # pending = int(use_cache and not has_key_cache(redis_key))

            # Execute flight and hotel retrieval in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                flight_future = executor.submit(self.get_flight)
                hotel_future = executor.submit(self.get_hotel, use_cache, iter)

                # Fetch results with timeout handling
                try:
                    flight = flight_future.result(timeout=2200)
                except TimeoutError:
                    print("------------ Flight Timeout ------------")
                    flight = {'go_flight': [], "return_flight": []}

                try:
                    hotel_result = hotel_future.result(timeout=2200)
                except TimeoutError:
                    print("------------ Hotel Timeout ------------")
                    hotel_result = []
                except Exception as e:
                    print(f"Hotel error: {e}")
                    hotel_result = []

                # Ensure all threads are properly closed
                executor.shutdown(wait=True)

            # Prepare provider data
            providers = {}
            hotel_result_prunned=[]
            for item in hotel_result:
                if 'NotExistProvider' in item:
                    providers[item['NotExistProvider']]={
                        'length':0,
                        'message': 'اتمام زمان',
                        'url': ''
                    }

                else:
                    hotel_result_prunned.append(item)
                    for provider in {room['provider'] for room in item['rooms']}:
                        if provider not in providers:
                            providers[provider] = {'length': 0, 'message': 'اتمام زمان', 'url': ''}
                        providers[provider]['length'] += 1
                        providers[provider]['message'] = ''

            result = {
                "flight": flight,
                "hotel": hotel_result_prunned,
                "providers": providers
            }

            # Cache the result
            # Run caching in a separate thread
            with ThreadPoolExecutor(max_workers=1) as executor_cache:
                executor_cache.submit(add_cache, redis_key, result)



        except Exception as e:
            print(f"Traceback details:\n{traceback.format_exc()}")
            return []

        return result


class BuildTourAnalysis():
    def __init__(self,start_date,end_date, source, target,night_count, adults):
        self.start_date = start_date
        self.end_date = end_date
        self.source = source
        self.target = target
        self.adults = adults
        self.night_count = night_count


    def get_flight(self,start_date,end_date):
        flight = Flight(start_date=start_date, end_date=end_date, source=self.source, target=self.target,
                        one_way=False)
        return flight.get_result()

    def get_hotel(self,start_date,end_date,use_cache,iter,isAnalysiss,hotelstarAnalysis,priorityTimestamp):
        hotel = Hotel(source=self.source, target=self.target, start_date=start_date, end_date=end_date,
                      adults=self.adults,use_cache=use_cache,isAnalysiss=isAnalysiss,hotelstarAnalysis=hotelstarAnalysis,
                      priorityTimestamp=priorityTimestamp)
        return hotel.get_result(iter)

    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime, timedelta

    def get_analysis(self, start_date, end_date, range_number=7, use_cache=True, hotelstarAnalysis=[],priorityTimestamp=1):
        print(f'Get Analysisssss {hotelstarAnalysis[0]}')
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        date_range = [(start_date + timedelta(days=date)).strftime("%Y-%m-%d") for date in range(range_number)]



        # Using ThreadPoolExecutor efficiently
        t1=datetime.now()
        with ThreadPoolExecutor(max_workers=min(len(date_range), 10)) as executor:
            futures = {
                executor.submit(self.get_result, start_date, use_cache, iter, True, hotelstarAnalysis,priorityTimestamp): start_date
                for iter, start_date in enumerate(date_range)
            }

            # Collect results with error handling
            result = {
                start_date: future.result() if (future.exception() is None) else []
                for future, start_date in futures.items()
            }

            # Ensure all threads are properly closed
            executor.shutdown(wait=True)
            logger.info(f' time BuildTour get_analysis --- {(datetime.now() - t1).total_seconds()}')


        return result



    def get_result(self, start_date, use_cache, iter, isAnalysiss=False, hotelstarAnalysis=[],priorityTimestamp=1):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = start_date_obj + timedelta(days=self.night_count)
        end_date = end_date_obj.strftime("%Y-%m-%d")

        #--------
        if (len(hotelstarAnalysis)!=0):
            redis_key = f"build_tour_{self.source}_{self.target}_{start_date}_{end_date}_{','.join(hotelstarAnalysis)}"

        else:
            redis_key = f"build_tour_{self.source}_{self.target}_{start_date}_{end_date}"
        #-----

        print(f'TimeStamp_Analysis ==== {priorityTimestamp}')

        # === Check Redis Cache First ===
        if use_cache and has_key_cache(redis_key):
            return get_cache(redis_key)

        results = {"flight": None, "hotel": None, "providers": {}}

        # === Submit Flight & Hotel Requests Asynchronously ===
        t1=datetime.now()
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                # executor.submit(self.get_flight, start_date, end_date): "flight",
                executor.submit(self.get_hotel, start_date, end_date, use_cache, iter, isAnalysiss,
                                hotelstarAnalysis,priorityTimestamp): "hotel"
            }

            # === Process Completed Tasks ===
            for future in as_completed(futures, timeout=220):  # Adjust timeout if needed
                task_type = futures[future]
                try:
                    results[task_type] = future.result()
                except Exception:
                    print(f"--------------------------------\n{task_type} time out or error\n{traceback.format_exc()}")
                    results[task_type] = {'go_flight': [], "return_flight": []} if task_type == "flight" else []

        logger.info(f' time BuildTour get_result --- {(datetime.now() - t1).total_seconds()}')
        # === Process Providers Efficiently ===
        t1=datetime.now()
        if results["hotel"]:
            results["providers"] = self.process_providers(results["hotel"])

        logger.info(f' time BuildTour process_providers --- {(datetime.now() - t1).total_seconds()}')
        # === Cache the Result in the Background ===
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(add_cache, redis_key, results)

        return results


    #???????????????????????????????????????????????????
    # ???????????????????????????????????????????????????
    # ???????????????????????????????????????????????????


    def process_providers(self, hotel_result):
        """ Optimized provider extraction with multithreading """
        providers = defaultdict(lambda: {'length': 0, 'message': 'اتمام زمان', 'url': ''})

        def process_item(item):
            return {a['provider'] for a in item['rooms']}

        with ThreadPoolExecutor() as executor:
            results = executor.map(process_item, hotel_result)

        for providers_set in results:
            for provider in providers_set:
                providers[provider]['length'] += 1
                providers[provider]['message'] = ''

        return dict(providers)


    def process_providers_old(self, hotel_result):
        """ Optimized provider extraction """
        providers = {}
        for item in hotel_result:
            for provider in {a['provider'] for a in item['rooms']}:
                providers.setdefault(provider, {'length': 0, 'message': 'اتمام زمان', 'url': ''})
                providers[provider]['length'] += 1
                providers[provider]['message'] = ''
        return providers
