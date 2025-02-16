import json
import traceback
from app_crawl.hotel.main import Hotel
from app_crawl.flight.main import Flight
from app_crawl.cache.cache import add_cache, get_cache, has_key_cache

from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime, timedelta
import traceback
from collections import defaultdict

# from monitoring import influx_grafana
class BuildTour:
    def __init__(self, source, target, start_date, end_date, adults):
        self.source = source
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults

    def get_flight(self):
        flight = Flight(start_date=self.start_date, end_date=self.end_date, source=self.source, target=self.target,
                        one_way=False)
        return flight.get_result()

    def get_hotel(self,use_cache,iter):
        hotel = Hotel(source=self.source, target=self.target, start_date=self.start_date, end_date=self.end_date,
                      adults=self.adults,use_cache=use_cache,isAnalysiss=False,hotelstarAnalysis=[])
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

            # Prepare provider data
            providers = {}
            for item in hotel_result:
                for provider in {room['provider'] for room in item['rooms']}:
                    if provider not in providers:
                        providers[provider] = {'length': 0, 'message': 'اتمام زمان', 'url': ''}
                    providers[provider]['length'] += 1
                    providers[provider]['message'] = ''

            result = {
                "flight": flight,
                "hotel": hotel_result,
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

    def get_result_old(self, use_cache=True,iter=1):
        try:
            # # ===return empty results===
            # flight = {'go_flight': [], "return_flight": []}
            # hotel_result = []
            # result = {
            #     "flight": flight,
            #     "hotel": hotel_result,
            #     'providers':{}
            #
            # }
            # return result
            # # ==========


            # redis_key = f"build_{self.start_date}_{self.end_date}"
            redis_key = f"build_tour_{self.source}_{self.target}_{self.start_date}_{self.end_date}" #?????
            # redis_key = f"build_tour_{self.source}_{self.target}_{start_date}_{end_date}" #?????

            # # # --- check from redis
            if has_key_cache(key=redis_key) and use_cache:
                return get_cache(key=redis_key)

            #--- consider also Pending caches ---
            pending=0
            if use_cache:
                if has_key_cache(key=redis_key):
                    return get_cache(key=redis_key)
                else:
                    pending=1
            # # # ---

            executor = ThreadPoolExecutor(max_workers=10)
            # ---
            flight = executor.submit(self.get_flight)
            hotel = executor.submit(self.get_hotel,use_cache,iter)
            # ---
            try:
                # 120
                flight = flight.result(timeout=220000)
            except:
                print("--------------------------------")
                print("flight time out")
                flight = {'go_flight': [], "return_flight": []}
            try:
                # 130
                hotel_result = hotel.result(timeout=2200000)
            except Exception as e:
                print("--------------------------------")
                print("hotel time out")
                print(str(e))
                hotel_result = []
            # ---
            result = {
                "flight": flight,
                "hotel": hotel_result,
                'providers':{}

            }
            #==== get provider lists ===
            providers={}
            for item in hotel_result:
                for porov in set([a['provider'] for a in item['rooms']]):
                    if (porov not in providers.keys()):
                        providers[porov]= {
                            'length':0,
                            'message':'اتمام زمان',
                            'url':''
                        }
                    providers[porov]['length']=providers[porov]['length']+1
                    providers[porov]['message']=''

            result['providers']=providers
            #=====
            #===== Disbale Caching ===
            add_cache(redis_key, result)
            #============
        except Exception as e:
            tb = traceback.format_exc()  # Get the full traceback as a string
            print(f"Traceback details:\n{tb}")
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

    def get_hotel(self,start_date,end_date,use_cache,iter,isAnalysiss,hotelstarAnalysis):
        hotel = Hotel(source=self.source, target=self.target, start_date=start_date, end_date=end_date,
                      adults=self.adults,use_cache=use_cache,isAnalysiss=isAnalysiss,hotelstarAnalysis=hotelstarAnalysis)
        return hotel.get_result(iter)

    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime, timedelta

    def get_analysis(self, start_date, end_date, range_number=7, use_cache=True, hotelstarAnalysis=[]):
        print(f'Get Analysisssss {hotelstarAnalysis[0]}')
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        date_range = [(start_date + timedelta(days=date)).strftime("%Y-%m-%d") for date in range(range_number)]

        # Using ThreadPoolExecutor efficiently
        with ThreadPoolExecutor(max_workers=min(len(date_range), 10)) as executor:
            futures = {
                executor.submit(self.get_result, start_date, use_cache, iter, True, hotelstarAnalysis): start_date
                for iter, start_date in enumerate(date_range)
            }

            # Collect results with error handling
            result = {
                start_date: future.result() if (future.exception() is None) else []
                for future, start_date in futures.items()
            }

        return result



    def get_analysis_old(self,start_date,end_date,range_number=7,use_cache=True,hotelstarAnalysis=[]):

        # return {}

        #
        #========== a simple result (OK hast)
        #
        # start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        # date_range = [(start_date + timedelta(days=date)).strftime("%Y-%m-%d") for date in range(range_number)]
        # #=== print date_range
        # for start_date in date_range:
        #     print(f'date_range ===  {str(start_date)}')
        #
        # result = {
        #     "2024-10-01": [
        #         {
        #             'price': 2181600,
        #             'hotel_name':"=هتل اطلس بندرعباس",
        #             'room_name': "Room A",
        #             'provider': "Provider A"
        #         }
        #     ],
        #     "2024-10-02": [
        #         {
        #             'price': 150,
        #             'hotel_name': "Hotel 2",
        #             'room_name': "Room B",
        #             'provider': "Provider B"
        #         }
        #     ],
        #     "2024-10-03": [
        #         {
        #             'price': 120,
        #             'hotel_name': "Hotel 3",
        #             'room_name': "Room C",
        #             'provider': "Provider C"
        #         }
        #     ]
        #
        # }
        # return result
        # with open('get_analysis_result_complete.json','r',encoding='utf8') as fp:
        #     res_json=json.load(fp)
        #
        # return res_json

        # #==================



        # range_number=1

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        date_range = [(start_date + timedelta(days=date)).strftime("%Y-%m-%d") for date in range(range_number)]
        # print(f'start_dateeeee ===  {str(start_date)}')


        # #=== print date_range
        # for start_date in date_range:
        #     print(f'date_range ===  {str(start_date)}')
        # #===


        # Submit tasks and map each future to its start_date
        futures_to_dates = {
            self.executor_analysis.submit(self.get_result, start_date, use_cache,iter,True,hotelstarAnalysis): start_date
            for iter,start_date in enumerate(date_range)
        }

        # Initialize an empty dictionary to store results with their corresponding start_date
        sami_result = {}

        # Retrieve results and populate sami_result
        for future, start_date in futures_to_dates.items():
            try:
                sami_result[start_date] = future.result()  # Store the result by start_date
            except Exception as e:
                print(f"Error for start_date {start_date}: {e}")
                sami_result[start_date] = []  # Optionally, store None or handle error as needed

        # Create the final result dictionary with date_range as keys
        result = {date: sami_result.get(date,[]) for date in date_range}

        return result

        #
        # #===instead ====
        # futures = [self.executor_analysis.submit(self.get_result,start_date,use_cache) for start_date in date_range]
        # sami_result = []
        # for future in as_completed(futures):
        #     try:
        #         result = future.result()  # This will block until the future is done
        #         sami_result.append(result)
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        #
        # #+================
        #
        # result = {date_range[index]: r for index, r in enumerate(sami_result)}
        # # add_dict_to_redis(redis_key, {'status': True, "data": result}, default_redis_expire)



        #========== results build (OK hast)

        # #=== dumps result into file
        # with open('get_analysis_result_complete.json','w',encoding='utf8') as json_file:
        #     json.dump(result,json_file)



        #------------- OLD code -------------
        # res={}
        # for day in result.keys():
        #     res[day]=[]
        #
        #     try:
        #         min_price_go=result[day]['flight']['go_flight'][0]['min_price']
        #         min_price_return=result[day]['flight']['return_flight'][0]['min_price']
        #     except:
        #         continue
        #
        #     for htl in  result[day]['hotel']:
        #         try:
        #
        #             oneItem = {}
        #             oneItem['hotel_name'] = htl['hotel_name']
        #             oneItem['hotel_star'] = htl['hotel_star']
        #
        #             # Finding the room with the minimum price and its index
        #             min_index, min_room = min(enumerate(htl['rooms']), key=lambda x: int(str(x[1]['price'])))
        #             min_price = int(str(min_room['price']))
        #
        #             # Setting details for the room with the minimum price
        #             oneItem['room_name'] = min_room['name']
        #             oneItem['provider'] = min_room['provider']
        #             oneItem['price'] = min_price / self.adults + min_price_go + min_price_return
        #
        #
        #             # oneItem={}
        #             # oneItem['hotel_name']=htl['hotel_name']
        #             # oneItem['room_name']=htl['rooms'][0]['name']  #???
        #             #
        #             # # Finding the minimum price in all rooms
        #             # min_price = min(int(str(room['price'])) for room in htl['rooms'])
        #             #
        #             # # Updating 'oneItem' with the minimum room price adjusted for adults, go, and return prices
        #             # oneItem['price'] = min_price / self.adults + min_price_go + min_price_return
        #             #
        #             #
        #             # # oneItem['price']=int(str(htl['rooms'][0]['price'])) / self.adults +  min_price_go+min_price_return
        #             # oneItem['provider']= htl['rooms'][0]['provider']
        #             # oneItem['hotel_star']= htl['hotel_star']
        #
        #             # print(htl['hotel_name'])
        #             res[day].append(oneItem)
        #         except:
        #             print('error in cal')
        #
        #
        #
        # # #=== dumps result into file
        # # with open('get_analysis_result_complete.json','w',encoding='utf8') as json_file:
        # #     json.dump(res,json_file)
        #
        # return res
        #----------------- OLD code --------------



        # result = {
        #     "2024-10-01": [
        #         {
        #             'price': 2181600,
        #             'hotel_name':"=هتل اطلس بندرعباس",
        #             'room_name': "Room A",
        #             'provider': "Provider A"
        #         }
        #     ],
        #     "2024-10-02": [
        #         {
        #             'price': 150,
        #             'hotel_name': "Hotel 2",
        #             'room_name': "Room B",
        #             'provider': "Provider B"
        #         }
        #     ],
        #     "2024-10-03": [
        #         {
        #             'price': 120,
        #             'hotel_name': "Hotel 3",
        #             'room_name': "Room C",
        #             'provider': "Provider C"
        #         }
        #     ]
        #
        # }
        # return result
        #=====================================


        # return {'status': True, "data": result}


    def get_result(self, start_date, use_cache, iter, isAnalysiss=False, hotelstarAnalysis=[]):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = start_date_obj + timedelta(days=self.night_count)
        end_date = end_date_obj.strftime("%Y-%m-%d")
        redis_key = f"build_tour_{self.source}_{self.target}_{start_date}_{end_date}"

        # === Check Redis Cache First ===
        if use_cache and has_key_cache(redis_key):
            return get_cache(redis_key)

        results = {"flight": None, "hotel": None, "providers": {}}

        # === Submit Flight & Hotel Requests Asynchronously ===
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(self.get_flight, start_date, end_date): "flight",
                executor.submit(self.get_hotel, start_date, end_date, use_cache, iter, isAnalysiss,
                                hotelstarAnalysis): "hotel"
            }

            # === Process Completed Tasks ===
            for future in as_completed(futures, timeout=220):  # Adjust timeout if needed
                task_type = futures[future]
                try:
                    results[task_type] = future.result()
                except Exception:
                    print(f"--------------------------------\n{task_type} time out or error\n{traceback.format_exc()}")
                    results[task_type] = {'go_flight': [], "return_flight": []} if task_type == "flight" else []

        # === Process Providers Efficiently ===
        if results["hotel"]:
            results["providers"] = self.process_providers(results["hotel"])

        # === Cache the Result in the Background ===
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(add_cache, redis_key, results)

        return results


    def get_result_old(self, start_date, use_cache, iter,isAnalysiss=False,hotelstarAnalysis=[]):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = str(start_date_obj + timedelta(days=self.night_count))
        redis_key = f"build_tour_{self.source}_{self.target}_{start_date}_{end_date}"

        # === Check Redis Cache First ===
        if use_cache and has_key_cache(redis_key):
            return get_cache(redis_key)

        # === Submit Tasks Asynchronously ===
        futures = {
            self.executor.submit(self.get_flight, start_date, end_date): "flight",
            self.executor.submit(self.get_hotel, start_date, end_date, use_cache, iter,isAnalysiss,hotelstarAnalysis): "hotel"
        }

        results = {"flight": None, "hotel": None, "providers": {}}

        # === Process Completed Tasks ===
        for future in as_completed(futures, timeout=220):  # Adjust timeout if needed
            task_type = futures[future]
            try:
                results[task_type] = future.result()
            except Exception as e:
                print(f"--------------------------------\n{task_type} time out or error\n{traceback.format_exc()}")
                results[task_type] = {'go_flight': [], "return_flight": []} if task_type == "flight" else []

        # === Process Providers Efficiently ===
        results["providers"] = self.process_providers(results["hotel"])

        # === Submit Cache Update Asynchronously ===
        self.executor.submit(add_cache, redis_key, results)

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



    def get_result_old(self,start_date,use_cache,iter):

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = str(start_date_obj + timedelta(days=self.night_count))

        redis_key = f"build_tour_{self.source}_{self.target}_{start_date}_{end_date}" #?????



        # --- check from redis
        if has_key_cache(key=redis_key) and use_cache:
            return get_cache(key=redis_key)
        # ---


        # ---
        flight = self.executor.submit(self.get_flight,start_date, end_date)
        hotel = self.executor.submit(self.get_hotel,start_date,end_date,use_cache,iter)
        # ---
        try:
            # 120
            flight = flight.result(timeout=220000)
        except:
            print("--------------------------------")
            print("flight time out")
            flight = {'go_flight': [], "return_flight": []}
        try:
            # 130
            hotel_result = hotel.result(timeout=2200000)
        except Exception as e:
            print("--------------------------------")
            print("hotel time out")
            tb = traceback.format_exc()  # Get the full traceback as a string
            print(f"Traceback details:\n{tb}")
            hotel_result = []
        # ---
        result = {
            "flight": flight,
            "hotel": hotel_result,
            'providers':{}

        }
        #==== get provider lists ===
        providers={}
        for item in hotel_result:
            for porov in set([a['provider'] for a in item['rooms']]):
                if (porov not in providers.keys()):
                    providers[porov]= {
                        'length':0,
                        'message':'اتمام زمان',
                        'url':''
                    }
                providers[porov]['length']=providers[porov]['length']+1
                providers[porov]['message']=''

        result['providers']=providers
        #=====
        #===== Disbale Caching ===
        caching = self.executor.submit(add_cache, redis_key, result)
        # add_cache(redis_key, result)
        #============

        return result