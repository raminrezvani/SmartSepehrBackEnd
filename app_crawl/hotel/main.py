from .Crawl_Alaedin_ALL_OK import Alaedin
# from .Crawl_trivago_Selenium_OK import Trivago
from .Crawl_Snapp_api_OK import Snapp
from .DNS_utls import DNS_mapping
# from .Hotel_flytoday import FlyToday
# from app_crawl.hotel.deltaban import Deltaban
from .booking import Booking
# from .alwin import Alwin24
from .alwin_calling_OK import Alwin
from .jimbo import Jimbo
from .moghim24 import Moghim24
from .eghamat24 import Eghamat24
from app_crawl.helpers import (add_dict_to_redis, get_dict_to_redis, check_redis_key, ready_sepehr_gsm_hotel_name,
                               ready_sepehr_hotel_name)
from app_crawl.gsm.data import hotels_GSM
from concurrent.futures import ThreadPoolExecutor
# from app_crawl.hotel.sepehr import SepehrHotel
from app_crawl.cookie.cookie_data import (RAHBAL, HRC, DAYAN, OMID_OJ, SEPID_PARVAZ, PARMIS, HAMSAFAR, MEHRAB,
                                          TAK_SETAREH, IMAN, FLAMINGO, SHAYAN_GASHT, DOLFIN, YEGANE_FARD,ERAM2MHD,TOURISTKISH,SAFIRAN,HAMOOD,MOEINDARBARI,DARVISHI)
from app_crawl.kih.data import hotels
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait
# from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
# from app_crawl.hotel.sepehr_standalone_Flask_OK import get_result as sepehr_get_result
import requests
import json
import traceback
import time
# executorHotel=ThreadPoolExecutor(max_workers=100)
import logging
import redis
from django.conf import settings
logger = logging.getLogger('django')

redis_client = redis.Redis(
    host=settings.REDIS_CONFIG['HOST'],
    port=settings.REDIS_CONFIG['PORT'],
    db=settings.REDIS_CONFIG['DB'],
    decode_responses=settings.REDIS_CONFIG['DECODE_RESPONSES']
)


SEPEHR_SERVICE_URL = f"{settings.PROVIDER_SERVICES['SEPEHR']['BASE_URL']}{settings.PROVIDER_SERVICES['SEPEHR']['ENDPOINTS']['HOTEL_SEARCH']}"
DELTABAN_SERVICE_URL = f"{settings.PROVIDER_SERVICES['DELTABAN']['BASE_URL']}{settings.PROVIDER_SERVICES['DELTABAN']['ENDPOINTS']['HOTEL_SEARCH']}"

class Hotel:
    def __init__(self, source, target, start_date, end_date, adults,use_cache,isAnalysiss=False,
                 hotelstarAnalysis=[],priorityTimestamp=1):
        self.source = source
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.redis_expire = 10*60  # 3 minutes
        self.use_cache=use_cache
        # self.isAnalysis=isAnalysis[0] if isAnalysis is tuple else isAnalysis ,   # because isAnalysis is a tuple
        self.isAnalysis=isAnalysiss
        # self.isAnalysis = isAnalysis[0][0] if isAnalysis is tuple else isAnalysis,  # because isAnalysis is a tuple
        # self.isAnalysis = self.isAnalysis[0] if self.isAnalysis is tuple else self.isAnalysis,  # because isAnalysis is a tuple

        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp=priorityTimestamp



        # ---- read from redis ---
        # (RAHBAL, HRC, DAYAN, OMID_OJ, SEPID_PARVAZ, PARMIS, HAMSAFAR, MEHRAB,
        #  TAK_SETAREH, IMAN, FLAMINGO, SHAYAN_GASHT, DOLFIN, YEGANE_FARD, ERAM2MHD, TOURISTKISH, SAFIRAN, HAMOOD,
        #  MOEINDARBARI, DARVISHI)
        # ???????????????????????????????
        
        try:
            self.DARVISHI = json.loads(redis_client.get('darvishi'))
        except:
            print(f'providerCode  darvishi __ not in Redis')
            self.DARVISHI=DARVISHI

        try:
            self.MOEINDARBARI = json.loads(redis_client.get('moeindarbari'))
        except:
            print(f'providerCode  moeindarbari __ not in Redis')
            self.MOEINDARBARI = MOEINDARBARI

        try:
            self.IMAN = json.loads(redis_client.get('iman'))
        except:
            print(f'providerCode  iman __ not in Redis')
            self.IMAN=IMAN

        try:
            self.FLAMINGO = json.loads(redis_client.get('flamingo'))
        except:
            print(f'providerCode  flamingo __ not in Redis')
            self.FLAMINGO = FLAMINGO



        try:
            self.YEGANE_FARD = json.loads(redis_client.get('yegane_fard'))
        except:
            print(f'providerCode  yegane_fard __ not in Redis')
            self.YEGANE_FARD = YEGANE_FARD


        try:
            self.HAMOOD = json.loads(redis_client.get('hamood'))
        except:
            print(f'providerCode  hamood __ not in Redis')
            self.HAMOOD = HAMOOD

        try:
            self.SAFIRAN = json.loads(redis_client.get('safiran'))
        except:
            print(f'providerCode  safiran __ not in Redis')
            self.SAFIRAN = SAFIRAN

        try:
            self.DOLFIN = json.loads(redis_client.get('dolfin'))
        except:
            print(f'providerCode  dolfin __ not in Redis')
            self.DOLFIN = DOLFIN


        try:
            self.RAHBAL = json.loads(redis_client.get('rahbal'))
        except:
            print(f'providerCode  rahbal __ not in Redis')
            self.RAHBAL = RAHBAL

        try:
            self.HRC = json.loads(redis_client.get('hrc'))
        except:
            print(f'providerCode  hrc __ not in Redis')
            self.HRC = HRC

        try:
            self.DAYAN = json.loads(redis_client.get('dayan'))
        except:
            print(f'providerCode  dayan __ not in Redis')
            self.DAYAN = DAYAN
        try:
            self.OMID_OJ = json.loads(redis_client.get('omid_oj'))
        except:
            print(f'providerCode  omid_oj __ not in Redis')
            self.OMID_OJ = OMID_OJ

        try:
            self.SEPID_PARVAZ = json.loads(redis_client.get('sepid_parvaz'))
        except:
            print(f'providerCode  sepid_parvaz __ not in Redis')
            self.SEPID_PARVAZ = SEPID_PARVAZ
        try:
            self.PARMIS = json.loads(redis_client.get('parmis'))
        except:
            print(f'providerCode  parmis __ not in Redis')
            self.PARMIS = PARMIS
        try:
            self.MEHRAB = json.loads(redis_client.get('mehrab'))
        except:
            print(f'providerCode  mehrab __ not in Redis')
            self.MEHRAB = MEHRAB

        try:
            self.HAMSAFAR = json.loads(redis_client.get('hamsafar'))
        except:
            print(f'providerCode  hamsafar __ not in Redis')
            self.HAMSAFAR = HAMSAFAR

        try:
            self.TAK_SETAREH = json.loads(redis_client.get('tak_setareh'))
        except:
            print(f'providerCode  tak_setareh __ not in Redis')
            self.TAK_SETAREH = TAK_SETAREH

        try:
            self.TOURISTKISH = json.loads(redis_client.get('kimiya'))
        except:
            print(f'providerCode  kimiya __ not in Redis')
            self.TOURISTKISH = TOURISTKISH

        try:
            self.ERAM2MHD = json.loads(redis_client.get('eram2mhd'))
        except:
            print(f'providerCode  eram2mhd __ not in Redis')
            self.ERAM2MHD = ERAM2MHD


        try:
            self.SHAYAN_GASHT = json.loads(redis_client.get('shayan_gasht'))
        except:
            print(f'providerCode  shayan_gasht __ not in Redis')
            self.SHAYAN_GASHT = SHAYAN_GASHT

        # ???????????????????????????
        # ------------




    #==== Threaded version ====
    from concurrent.futures import ThreadPoolExecutor
    from collections import defaultdict

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from collections import defaultdict
    import traceback

    
    # Replace the direct sepehr_get_result calls with this helper function
    def _call_sepehr_service(self, cookie, provider_name):
        try:
            payload = {
                "target": self.target,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "adults": self.adults,
                "cookie": cookie,
                "provider_name": provider_name,
                "is_analysis": self.isAnalysis,
                "hotelstar_analysis": self.hotelstarAnalysis,
                "priority_timestamp": self.priorityTimestamp
            }

            response = requests.post(
                SEPEHR_SERVICE_URL,
                json=payload,
                timeout=60
            )

            if response.ok:
                result = response.json()
                if result.get('status'):
                    return result.get('data', [])
            return []
        except Exception as e:
            logger.error(f"Error calling Sepehr service for {provider_name}: {str(e)}")
            return []

    
    # Add this method to Hotel class
    def _call_deltaban_service(self):
        try:
            payload = {
                "target": self.target,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "adults": self.adults,
                "is_analysis": self.isAnalysis,
                "hotelstar_analysis": self.hotelstarAnalysis,
                "priority_timestamp": self.priorityTimestamp,
                "use_cache": self.use_cache
            }

            response = requests.post(
                DELTABAN_SERVICE_URL,
                json=payload,
                # timeout=30
            )

            if response.ok:
                result = response.json()
                if result.get('status'):
                    return result.get('data', [])
            return []
        except Exception as e:
            logger.error(f"Error calling Deltaban service: {str(e)}")
            return []

    def read_data_ALLDestination(self, data):
        print('start mapping .....')
        ds = DNS_mapping(self.target)
        result = defaultdict(lambda: {"rooms": []})  # Avoid KeyErrors

        def process_hotel(hotel):
            try:

                if ('ساسان' in hotel['hotel_name']):
                    print('hotel sasan')

                hotel_name_redis_key = f"hotel_name:{hotel['hotel_name']}_{self.target}"
                hotel_name_redis = redis_client.get(hotel_name_redis_key)
                if not hotel_name_redis:

                    hotelname, hotelStar = ds.check_hotelName(hotel['hotel_name'], self.target)
                    redis_client.set(hotel_name_redis_key, json.dumps((hotelname, hotelStar)))

                    #---- for asli hotel name ----------
                    asli_hotelname=f"asli_hotel:{hotelname}"
                    res_redis_aslihotelname=redis_client.get(asli_hotelname)
                    if not res_redis_aslihotelname:
                        redis_client.set(asli_hotelname, json.dumps([hotel['hotel_name']]))
                    else:
                        existing_list = json.loads(res_redis_aslihotelname)
                        if hotel['hotel_name'] not in existing_list:  # Avoid duplicates
                            existing_list.append(hotel['hotel_name'])
                            redis_client.set(asli_hotelname, json.dumps(existing_list))
                    #-----------------------


                else:
                    hotelname, hotelStar=json.loads(hotel_name_redis)

                # hotelname, hotelStar = ds.check_hotelName(hotel['hotel_name'], self.target)
                if not hotelname:
                    return None  # Skip if no valid hotel name

                default_data = {
                    "hotel_name": hotelname,
                    "hotel_star": hotelStar,
                    "min_price": float('inf'),
                    "rooms": [],
                    "provider": hotel['provider']
                }

                hotel_name = hotelname.strip()
                hotel_rooms = []
                for room in hotel['rooms']:
                    try:
                        room['price'] = int(room['price'])
                    except:
                        room['price'] = 999999999  # Avoid JSON float error

                    hotel_rooms.append(room)

                return hotel_name, default_data, hotel_rooms
            except Exception as e:
                # print(f"Traceback details:\n{traceback.format_exc()}")

                return None

        with ThreadPoolExecutor(max_workers=40) as executor:
            futures = {executor.submit(process_hotel, hotel): hotel for hotel_list in data for hotel in hotel_list}

            for future in as_completed(futures):
                result_data = future.result()
                if result_data:
                    hotel_name, default_data, hotel_rooms = result_data
                    if hotel_name not in result:
                        result[hotel_name].update(default_data)
                    result[hotel_name]['rooms'].extend(hotel_rooms)

        # Calculate min price for each hotel
        for hotel_name, hotel_data in result.items():
            min_price = min((float(room['price']) for room in hotel_data['rooms']), default=999999999)
            hotel_data['min_price'] = min_price

        # Sort hotels by min_price
        sorted_hotels = sorted(result.items(), key=lambda x: x[1]['min_price'])
        return [hotel[1] for hotel in sorted_hotels]



    def get_ALLDestination_data(self,iter):
        try:
            t1 = datetime.now()
            results = []


            hotel_tasks = {
                # "deltaban": 1,  # Change this from Deltaban class instance to 1
                "alwin": Alwin(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache),
                # "snapp" : Snapp(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache),
                # "alaedin": Alaedin(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache),
                # "eghamat": Eghamat24(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache),
                # "booking": Booking(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache),
                # "jimboo": Jimbo(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp,self.use_cache),
                # # # #
                # "darvishi": 1,
                # "moeindarbari": 1,
                # "rahbal":1,
                # "hrc": 1,
                # "dayan": 1,
                # "omid_oj": 1,
                # "sepid_parvaz":1,
                # "parmis":1,
                # "mehrab": 1,
                # "hamsafar":1,
                # "tak_setareh":1,
                # "kimiya": 1,
                # "eram2mhd": 1,
                # "shayan_gasht": 1,
                # "iman": 1,
                # "flamingo": 1,
                # "yegane_fard": 1,
                # "hamood": 1,
                # "safiran": 1,
                # "dolfin": 1
            }

            # print(f' time Create hotel_tasks --- {(datetime.now()-t1).total_seconds()} ')
            logger.info(f' time Create hotel_tasks --- {(datetime.now()-t1).total_seconds()}' )
            provider_status = {}
            startTime = datetime.now()


            with ThreadPoolExecutor(max_workers=min(len(hotel_tasks.keys()), 50)) as executor:
                fu={}
                for key , task in hotel_tasks.items():
                    if key == 'darvishi' and task== 1:
                        fu[executor.submit(
                            self._call_sepehr_service, self.DARVISHI,
                             'darvishi'
                            )]='darvishi'

                    elif key == 'moeindarbari' and task==1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.MOEINDARBARI, 
                            'moeindarbari'
                        )]='moeindarbari'

                    elif key == 'rahbal' and task==1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.RAHBAL,
                            'rahbal'
                        )]='rahbal'

                    elif key == 'hrc' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.HRC,
                            'hrc'
                        )]='hrc'
                    elif key == 'dayan' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.DAYAN,
                            'dayan'
                        )]='dayan'
                    elif key == 'omid_oj' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.OMID_OJ,
                            'omid_oj'
                        )]='omid_oj'
                    elif key == 'sepid_parvaz' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.SEPID_PARVAZ,
                            'sepid_parvaz'
                        )]='sepid_parvaz'
                    elif key == 'parmis' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.PARMIS,
                            'parmis'
                        )]='parmis'
                    elif key == 'mehrab' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.MEHRAB,
                            'mehrab'
                        )]='mehrab'
                    elif key == 'hamsafar' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.HAMSAFAR,
                            'hamsafar'
                        )]='hamsafar'
                    elif key == 'tak_setareh' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.TAK_SETAREH,
                            'tak_setareh'
                        )]='tak_setareh'
                    elif key == 'kimiya' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.TOURISTKISH,
                            'kimiya'
                        )]='kimiya'
                    elif key == 'eram2mhd' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.ERAM2MHD,
                            'eram2mhd'
                        )]='eram2mhd'
                    elif key == 'shayan_gasht' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.SHAYAN_GASHT,
                            'shayan_gasht'
                        )]='shayan_gasht'
                    elif key == 'iman' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.IMAN,
                            'iman'
                        )]='iman'
                    elif key == 'flamingo' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.FLAMINGO,
                            'flamingo'
                        )]='flamingo'
                    elif key == 'yegane_fard' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.YEGANE_FARD,
                            'yegane_fard'
                        )]='yegane_fard'
                    elif key == 'hamood' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.HAMOOD,
                            'hamood'
                        )]='hamood'
                    elif key == 'safiran' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.SAFIRAN,
                            'safiran'
                        )]='safiran'
                    elif key == 'dolfin' and task == 1:
                        fu[executor.submit(
                            self._call_sepehr_service,
                            self.DOLFIN,
                            'dolfin'
                        )]='dolfin'
                     # And in the executor section, add a new elif condition:
                    elif key == 'deltaban' and task == 1:
                        fu[executor.submit(
                            self._call_deltaban_service
                        )] = 'deltaban'
                    else:
                        fu[executor.submit(task.get_result)]=key

                #--- OLD ---
                # futures = {executor.submit(task.get_result): key for key, task in hotel_tasks.items()}
                # print(f' time Assign tasks --- {(datetime.now() - startTime).total_seconds()} ')
                logger.info(f' time Assign tasks --- {(datetime.now() - startTime).total_seconds()}' )



                #---New
                result_notExistProviders=[]
                # Wait for all futures to complete, but only for 60 seconds
                if (self.isAnalysis==False):
                    completed, pending = wait(fu.keys(), timeout=60)
                    # Process results from completed futures
                    for future in completed:
                        key = fu[future]
                        try:
                            result = future.result()  # Get result (no timeout needed here since it's already completed)
                            if isinstance(result, dict):
                                if len(result['data']) != 0:
                                    results.append(result)
                                else:
                                    result_notExistProviders.append({'NotExistProvider': key, 'data': [], 'status': 'اتمام زمان'})
                                    # print('OLD one')
                            else:
                                flag_data = any(it['rooms'] and len(it['rooms']) != 0 for it in result)

                                if flag_data:
                                    results.append(result)
                                    logger.info(f'Length hotel results --- {len(result)}')
                                else:
                                    result_notExistProviders.append(
                                        {'NotExistProvider': key, 'data': [], 'status': 'اتمام زمان'})




                            logger.info(f' Processed {key} --- {(datetime.now() - t1).total_seconds()}')
                        except Exception as e:
                            print(f"Error in {key}: {e}")
                            # results.append([])

                    # Log any pending tasks that didn't complete within 60 seconds
                    for future in pending:
                        key = fu[future]
                        logger.info(f"Timeout: {key} did not complete within 60 seconds")
                        # Optionally append a timeout result
                        # results.append({'provider': key, 'data': [], 'status': 'timeout'})

                    logger.info(f' time hotel processing completed --- {(datetime.now() - t1).total_seconds()}')
                    #----
                else:  # self.isAnalysis==True
                    #---------------
                    t1=datetime.now()
                    for future in as_completed(fu):
                        # key = fu[future]
                        try:
                            result=future.result()   # Set timeout for each provider
                            if  isinstance(result, dict):
                                if (len(result['data'])!=0):
                                    results.append(result)
                            else:
                                results.append(result)
                                logger.info(f' Length hotel results --- {len(result)}')

                            logger.info(f' time hotel isinstance(result, dict) --- {(datetime.now() - t1).total_seconds()}')

                            # spendTime = (datetime.now() - startTime).total_seconds()
                            # print(f'{key} ----- > spend:  {spendTime}')
                            # logger.info(f'{key} ----- > spend:  {spendTime}')
                        except Exception as e:
                            print(f"Error in er: {e}")
                            # results.append([])
                    # executor.shutdown(wait=False)
                    logger.info(f' time hotel as_completed --- {(datetime.now() - t1).total_seconds()}')
                #--



            t1=datetime.now()
            temp=self.read_data_ALLDestination(results)
            # print(f' time read_data_ALLDestination --- {(datetime.now() - t1).total_seconds()} ')
            logger.info(f' time read_data_ALLDestination --- {(datetime.now() - t1).total_seconds()}')


            #----------------------
            # add result_notExistProviders
            temp.extend(result_notExistProviders)
            #------------------


            return temp

        except Exception as e:
            # Log the error and the line number
            print(f"An error occurred: {e}")
            tb = traceback.format_exc()  # Get the full traceback as a string
            print(f"Traceback details:\n{tb}")

            return []

    #====


    def get_result(self,iter):

        if (len(self.hotelstarAnalysis)!=0):
            redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{','.join(self.hotelstarAnalysis)}"
        else:
            redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}"



        t1=datetime.now()
        # Check cache first
        if self.use_cache:
            cached_result = get_dict_to_redis(redis_key) if check_redis_key(redis_key) else None
            if cached_result is not None:
                return cached_result
        logger.info(f' time hotel redis_cache --- {(datetime.now() - t1).total_seconds()}')

        t1=datetime.now()
        # Fetch new data
        result = self.get_ALLDestination_data(iter)
        logger.info(f' time hotel get_ALLDestination_data --- {(datetime.now() - t1).total_seconds()}')

        # Cache the result asynchronously if valid
        # Optimized Threading: Uses a single worker since Redis operations are I/O bound.
        #Faster Lookups: Only checks Redis once and avoids redundant keys
        t1 = datetime.now()
        if result:
            print('start caching ..........')
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(add_dict_to_redis, redis_key, result, self.redis_expire)

        logger.info(f' time hotel beforeSend --- {(datetime.now() - t1).total_seconds()}')

        return result


    def get_result_old(self,iter):


        redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}"
        if self.use_cache and check_redis_key(redis_key):
            return get_dict_to_redis(redis_key)
        else:

            result = self.get_ALLDestination_data(iter)
            #== Multi Thread ===
            print('start caching ..........')
            if len(result):
                with ThreadPoolExecutor(max_workers=100) as executorr:
                    executorr.submit(add_dict_to_redis, redis_key, result, self.redis_expire)  # bayad doing ha delete shavad!! (OK)
            #=====
            #

            return result
