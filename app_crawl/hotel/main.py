from .Crawl_Alaedin_ALL_OK import Alaedin
# from .Crawl_trivago_Selenium_OK import Trivago
from .Crawl_Snapp_api_OK import Snapp
from .DNS_utls import DNS_mapping
# from .Hotel_flytoday import FlyToday
from .deltaban import Deltaban
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
from app_crawl.hotel.sepehr import SepehrHotel
from app_crawl.cookie.cookie_data import (RAHBAL, HRC, DAYAN, OMID_OJ, SEPID_PARVAZ, PARMIS, HAMSAFAR, MEHRAB,
                                          TAK_SETAREH, IMAN, FLAMINGO, SHAYAN_GASHT, DOLFIN, YEGANE_FARD,ERAM2MHD,TOURISTKISH,SAFIRAN,HAMOOD,MOEINDARBARI,DARVISHI)
from app_crawl.kih.data import hotels
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait
# from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from app_crawl.hotel.sepehr_standalone import get_result as sepehr_get_result

import traceback
import time
# executorHotel=ThreadPoolExecutor(max_workers=100)
import logging
logger = logging.getLogger('django')
class Hotel:
    def __init__(self, source, target, start_date, end_date, adults,use_cache,isAnalysiss=False,hotelstarAnalysis=[],priorityTimestamp=1):
        self.source = source
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.redis_expire = 10*60  # 3 minutes
        self.use_cache=use_cache,
        # self.isAnalysis=isAnalysis[0] if isAnalysis is tuple else isAnalysis ,   # because isAnalysis is a tuple
        self.isAnalysis=isAnalysiss
        # self.isAnalysis = isAnalysis[0][0] if isAnalysis is tuple else isAnalysis,  # because isAnalysis is a tuple
        # self.isAnalysis = self.isAnalysis[0] if self.isAnalysis is tuple else self.isAnalysis,  # because isAnalysis is a tuple

        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp=priorityTimestamp
    #==== Threaded version ====
    from concurrent.futures import ThreadPoolExecutor
    from collections import defaultdict

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from collections import defaultdict
    import traceback

    def read_data_ALLDestination(self, data):
        print('start mapping .....')
        ds = DNS_mapping(self.target)
        result = defaultdict(lambda: {"rooms": []})  # Avoid KeyErrors

        def process_hotel(hotel):
            try:
                hotelname, hotelStar = ds.check_hotelName(hotel['hotel_name'], self.target)
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




    #
    # def read_data_ALLDestination_old(self, data):
    #     data=data[0]
    #     print('start mapping .....')
    #     ds = DNS_mapping(self.target)
    #     result = defaultdict(lambda: {"rooms": []})  # Use defaultdict to avoid KeyErrors
    #
    #     def process_hotel(hotel):
    #         try:
    #             hotelname, hotelStar = ds.check_hotelName(hotel['hotel_name'], self.target)
    #             if not hotelname:
    #                 return None  # Skip if no valid hotel name
    #
    #
    #             try:
    #                 default_data = {
    #                     "hotel_name": hotelname,
    #                     "hotel_star": hotelStar,
    #                     "min_price": hotel['rooms'][0].get('price', 999999999),
    #                     "rooms": [],
    #                     "provider": hotel['provider']
    #                 }
    #             except:
    #                 return None
    #
    #             hotel_name = hotelname.strip()
    #             hotel_rooms = []
    #             for room in hotel['rooms']:
    #                 try:
    #                     room['price'] = int(room['price'])
    #                 except:
    #                     room['price'] = 9999999999999
    #
    #                 # #==== Check RoomName is for two adults
    #                 # if (
    #                 #         'یک ' in room['name'] or
    #                 #         ' یک' in room['name'] or
    #                 #         ' یک ' in room['name']
    #                 # ):
    #                 #     continue
    #                 # #===============================
    #
    #                 hotel_rooms.append(room)
    #
    #             # Update result with the default data and rooms
    #             return hotel_name, default_data, hotel_rooms
    #         except Exception as e:
    #             tb = traceback.format_exc()  # Get the full traceback as a string
    #             print(f"Traceback details:\n{tb}")
    #
    #             return None
    #
    #     # with ThreadPoolExecutor(max_workers=40) as executor:
    #     futures = [executorHotel.submit(process_hotel, hotel) for hotel in data]
    #     for future in futures:
    #         result_data = future.result()
    #         if result_data:
    #             hotel_name, default_data, hotel_rooms = result_data
    #             if hotel_name not in result:
    #                 result[hotel_name].update(default_data)
    #             result[hotel_name]['rooms'].extend(hotel_rooms)
    #
    #     # Calculate the minimum price for each hotel
    #     for hotel_name, hotel_data in result.items():
    #         min_price = float('inf')
    #         for room in hotel_data['rooms']:
    #             try:
    #                 room_price = float(room['price'])
    #             except:
    #                 room['price'] = 999999999
    #                 room_price = room['price']
    #             if room_price < min_price:
    #                 min_price = room_price
    #         hotel_data['min_price'] = min_price
    #
    #     # Sort hotels by min_price
    #     sorted_hotels = sorted(result.items(), key=lambda x: x[1]['min_price'])
    #     sorted_hotels_dict = dict(sorted_hotels)
    #
    #     return list(sorted_hotels_dict.values())

    # #== OLD version ===
    # def read_data_ALLDestination(self,data):
    #
    # #==== ??????????????? Multi-Threded ----------
    #
    # #????????????????????
    #
    #
    #
    #     ds = DNS_mapping()
    #     result = {}
    #     for hotel in data:
    #         try:
    #             #=
    #             hotelname,hotelStar=ds.check_hotelName(hotel['hotel_name'], self.target)
    #             # print(f'{hotel["hotel_name"]} -----> {hotelname}')
    #             # ---
    #             default_data = {
    #                 "hotel_name":  hotelname,
    #                 "hotel_star": hotelStar,
    #                 "min_price": hotel['rooms'][0]['price'],
    #                 "rooms": [],
    #                 "provider": hotel['provider']
    #             }
    #
    #             if default_data['hotel_name']=='':
    #                 continue
    #
    #             # ---
    #             roominserted=0
    #             hotel_name = default_data['hotel_name'].strip()
    #             if hotel_name not in result.keys():
    #                 result[hotel_name] = default_data
    #             else:
    #                 for room in hotel['rooms']:
    #                     try:
    #                         room['price']=int(room['price'])
    #                     except:
    #                         room['price']=9999999999999
    #                     result[hotel_name]['rooms'].append(room)
    #
    #                     roominserted=1
    #
    #             # Check if both values are numeric
    #             if not str(hotel['min_price']).isdigit():
    #                 hotel['min_price']=9999999999999
    #
    #             if not str(result[hotel_name]['min_price']).isdigit():
    #                 result[hotel_name]['min_price']=9999999999999
    #
    #             # ---
    #             if (roominserted==0):
    #                 for room in hotel['rooms']:
    #                     room['price'] = int(room['price'])
    #                     result[hotel_name]['rooms'].append(room)
    #
    #             # ---
    #         except:
    #             continue
    #
    #
    #     #Overall------- Update all Min_price
    #     for htl in list(result.keys()):
    #         min_price=float('inf')
    #         for rom in result[htl]['rooms']:
    #             try:
    #                 room_price=float(rom['price'])
    #             except:
    #                 rom['price'] = 999999999
    #                 room_price = float(rom['price'])
    #
    #             if (room_price<min_price):
    #                 result[htl]['min_price']=room_price
    #                 min_price=room_price
    #
    #     #---------------------
    #
    #
    #     #=== sort based on min_price
    #     # Sort hotels by min_price
    #     sorted_hotels = sorted(result.items(), key=lambda x: x[1]['min_price'])
    #     sorted_hotels_dict = dict(sorted_hotels)
    #
    #
    #     # #=== Save to disk
    #     # import json
    #     # aa=json.dumps(sorted_hotels_dict)
    #     # fp=open('sorted_hotels_dict.json','w',encoding='utf8')
    #     # fp.write(aa)
    #     # fp.close()
    #     # #======
    #
    #     #===
    #     return list(sorted_hotels_dict.values())
    #

    #
    # def read_data_GSM(self,data):
    #     ds = DNS_mapping(self.target)
    #     result = {}
    #     for hotel in data:
    #
    #         try:
    #             # hotel_name = ready_sepehr_gsm_hotel_name(hotel['hotel_name'])
    #             # ---
    #             default_data = {
    #                 "hotel_name":  ds.check_hotelName(hotel['hotel_name'],'GSM'),
    #                 "hotel_star": hotel['hotel_star'],
    #                 "min_price": int(hotel['min_price']),
    #                 "rooms": [],
    #                 "provider": hotel['provider']
    #             }
    #             # ---
    #             # found = 0
    #             # #=== Read DNS ===
    #             # hotels_DNS=hotels_GSM
    #             # #========
    #             #
    #             # for key, value in hotels_DNS.items():
    #             #     try:
    #             #         system_provider = value[hotel['provider']]
    #             #     except:
    #             #         # === Default DNS
    #             #         system_provider = key.replace('هتل', '').replace('کیش', '').strip()
    #             #         # ====
    #             #         # continue
    #             #
    #             #     if system_provider:
    #             #         if system_provider.strip() in hotel_name:
    #             #             default_data['hotel_name'] = key
    #             #             default_data['hotel_star'] = value['hotel_star']
    #             #             found = 1
    #             #
    #             # #-----
    #             # if found == 0:  # chizi peyda nashod
    #             #     continue
    #             if default_data['hotel_name']=='':
    #                 continue
    #
    #             # ---
    #             hotel_name = default_data['hotel_name']
    #             if hotel_name not in result.keys():
    #                 result[hotel_name] = default_data
    #             # ---
    #             if hotel['min_price'] < result[hotel_name]['min_price']:
    #                 result[hotel_name]['min_price'] = hotel['min_price']
    #             # ---
    #             for room in hotel['rooms']:
    #                 result[hotel_name]['rooms'].append(room)
    #             # ---
    #             # for key, value in hotels.items():
    #             #     system_provider = value[hotel['provider']]
    #             #     if system_provider:
    #             #         if system_provider.strip() in hotel_name:
    #             #             default_data['hotel_name'] = key
    #             #             default_data['hotel_star'] = value['hotel_star']
    #         except:
    #             continue
    #     return list(result.values())


    #
    # def ready_data(self,data, target):
    #
    #
    #
    #     result = {}
    #     for hotel in data:
    #
    #         try:
    #             # ----
    #             if target == "GSM":
    #                 hotel_name = ready_sepehr_gsm_hotel_name(hotel['hotel_name'])
    #             elif target == "KIH":
    #                 hotel_name = ready_sepehr_hotel_name(hotel['hotel_name'])
    #             else:
    #                 return []
    #             # ---
    #             default_data = {
    #                 "hotel_name": hotel_name,
    #                 "hotel_star": hotel['hotel_star'],
    #                 "min_price": hotel['min_price'],
    #                 "rooms": [],
    #                 "provider": hotel['provider']
    #             }
    #             # ---
    #             found = 0
    #             #=== Read DNS ===
    #             # kih -->data.py
    #             # gsm -> ??????
    #             #==========
    #             hotels_DNS=hotels
    #             if (target=="GSM"):
    #                 hotels_DNS=hotels_GSM
    #             #========
    #
    #             for key, value in hotels_DNS.items():
    #                 try:
    #                     system_provider = value[hotel['provider']]
    #                 except:
    #                     # === Default DNS
    #                     system_provider = key.replace('هتل', '').replace('کیش', '').strip()
    #                     # ====
    #                     # continue
    #
    #                 if system_provider:
    #                     if system_provider.strip() in hotel_name:
    #                         default_data['hotel_name'] = key
    #                         default_data['hotel_star'] = value['hotel_star']
    #                         found = 1
    #
    #             #-----
    #             if found == 0:  # chizi peyda nashod
    #                 continue
    #
    #             # ---
    #             hotel_name = default_data['hotel_name']
    #             if hotel_name not in result.keys():
    #                 result[hotel_name] = default_data
    #             # ---
    #             if hotel['min_price'] < result[hotel_name]['min_price']:
    #                 result[hotel_name]['min_price'] = hotel['min_price']
    #             # ---
    #             for room in hotel['rooms']:
    #                 result[hotel_name]['rooms'].append(room)
    #             # ---
    #             # for key, value in hotels.items():
    #             #     system_provider = value[hotel['provider']]
    #             #     if system_provider:
    #             #         if system_provider.strip() in hotel_name:
    #             #             default_data['hotel_name'] = key
    #             #             default_data['hotel_star'] = value['hotel_star']
    #         except:
    #             continue
    #     return list(result.values())
    # #
    # def ready_data_old(self, data, target):
    #     result = {}
    #     for hotel in data:
    #         try:
    #             # ----
    #             if target == "GSM":
    #                 hotel_name = ready_sepehr_gsm_hotel_name(hotel['hotel_name'])
    #             elif target == "KIH":
    #                 hotel_name = ready_sepehr_hotel_name(hotel['hotel_name'])
    #             else:
    #                 return []
    #             # ---
    #             default_data = {
    #                 "hotel_name": hotel_name,
    #                 "hotel_star": hotel['hotel_star'],
    #                 "min_price": hotel['min_price'],
    #                 "rooms": [],
    #                 "provider": hotel['provider']
    #             }
    #             # ---
    #             for key, value in hotels.items():
    #                 system_provider = value[hotel['provider']]
    #                 if system_provider:
    #                     if system_provider.strip() in hotel_name:
    #                         default_data['hotel_name'] = key
    #                         default_data['hotel_star'] = value['hotel_star']
    #             # ---
    #             hotel_name = default_data['hotel_name']
    #             if hotel_name not in result.keys():
    #                 result[hotel_name] = default_data
    #             # ---
    #             if hotel['min_price'] < result[hotel_name]['min_price']:
    #                 result[hotel_name]['min_price'] = hotel['min_price']
    #             # ---
    #             for room in hotel['rooms']:
    #                 result[hotel_name]['rooms'].append(room)
    #             # ---
    #             # for key, value in hotels.items():
    #             #     system_provider = value[hotel['provider']]
    #             #     if system_provider:
    #             #         if system_provider.strip() in hotel_name:
    #             #             default_data['hotel_name'] = key
    #             #             default_data['hotel_star'] = value['hotel_star']
    #         except:
    #             continue
    #     return list(result.values())
    #
    # def get_kih_data(self):
    #     result = []
    #     # ---
    #     with ThreadPoolExecutor(max_workers=85) as executor:
    #         # # #
    #
    #         #=== Eghamat24========
    #         eghamat = Eghamat24(self.target, self.start_date, self.end_date, self.adults)
    #         eghamat = executor.submit(eghamat.get_result)
    #         #====================
    #
    #
    #         # --- moghim24
    #         moghim = Moghim24(self.target, self.start_date, self.end_date, self.adults)
    #         moghim = executor.submit(moghim.get_result)
    #         #
    #         # # # --- deltaban
    #         deltaban = Deltaban(self.target, self.start_date, self.end_date, self.adults)
    #         deltaban = executor.submit(deltaban.get_result)
    #         # # --- alwin
    #         alwin = Alwin(self.target, self.start_date, self.end_date, self.adults)
    #         alwin = executor.submit(alwin.get_result)
    #         # # --- booking
    #         booking = Booking(self.target, self.start_date, self.end_date, self.adults)
    #         booking = executor.submit(booking.get_result)
    #         # # --- rahbal
    #         rahbal = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal')
    #         rahbal = executor.submit(rahbal.get_result)
    #         # --- HRC
    #         hrc = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HRC, 'hrc')
    #         hrc = executor.submit(hrc.get_result)
    #         # --- DAYAN
    #         dayan = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DAYAN, 'dayan')
    #         dayan = executor.submit(dayan.get_result)
    #         # --- OMID_OJ
    #         omid_oj = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, OMID_OJ, 'omid_oj')
    #         omid_oj = executor.submit(omid_oj.get_result)
    #         # --- SEPID_PARVAZ
    #         sepid_parvaz = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SEPID_PARVAZ,
    #                                    'sepid_parvaz')
    #         sepid_parvaz = executor.submit(sepid_parvaz.get_result)
    #         # --- PARMIS
    #         parmis = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, PARMIS, 'parmis')
    #         parmis = executor.submit(parmis.get_result)
    #         # --- MEHRAB
    #         mehrab = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab')
    #         mehrab = executor.submit(mehrab.get_result)
    #         # --- HAMSAFAR
    #         hamsafar = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMSAFAR, 'hamsafar')
    #         hamsafar = executor.submit(hamsafar.get_result)
    #         # --- TAK_SETAREH
    #         tak_setareh = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,
    #                                   'tak_setareh')
    #         tak_setareh = executor.submit(tak_setareh.get_result)
    #
    #         # --- Kimiya
    #         kimiya = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TOURISTKISH,
    #                                   'kimiya')
    #         kimiya = executor.submit(kimiya.get_result)
    #
    #         # --- Eram
    #         eram2mhd = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, ERAM2MHD,
    #                                   'eram2mhd')
    #         eram2mhd = executor.submit(eram2mhd.get_result)
    #
    #         # --- SHAYAN GASHT
    #         shayan_gasht = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,
    #                                    'shayan_gasht')
    #         shayan_gasht = executor.submit(shayan_gasht.get_result)
    #
    #
    #         #--- eghamat24
    #         try:
    #             eghamat=eghamat.result(timeout=10000)
    #         except:
    #             eghamat=[]
    #
    #
    #         #--- moghim24
    #         try:
    #             kimiya=kimiya.result(timeout=1000)
    #         except:
    #             kimiya=[]
    #
    #         try:
    #             eram2mhd=eram2mhd.result(timeout=1000)
    #         except:
    #             eram2mhd=[]
    #         try:
    #             shayan_gasht=shayan_gasht.result(timeout=1000)
    #         except:
    #             shayan_gasht=[]
    #
    #         #--- moghim24
    #         try:
    #             moghim=moghim.result(timeout=1000)
    #         except:
    #             moghim=[]
    #
    #         #
    #         # --- deltaban
    #         try:
    #             deltaban = deltaban.result(timeout=4000)
    #         except:
    #             deltaban = []
    #         # # # --- alwin
    #         try:
    #             alwin = alwin.result(timeout=400000)
    #         except:
    #             alwin = []
    #         # # --- booking
    #         try:
    #             booking = booking.result(timeout=400000)
    #         except:
    #             booking = []
    #         # --- rahbal
    #         try:
    #             rahbal = rahbal.result(timeout=4000)
    #         except:
    #             rahbal = []
    #         # --- hrc
    #         try:
    #             hrc = hrc.result(timeout=40)
    #         except:
    #             hrc = []
    #         # --- dayan
    #         try:
    #             dayan = dayan.result(timeout=4000)
    #         except:
    #             dayan = []
    #         # --- omid_oj
    #         try:
    #             omid_oj = omid_oj.result(timeout=4000)
    #         except:
    #             omid_oj = []
    #         # --- sepid_parvaz
    #         try:
    #             sepid_parvaz = sepid_parvaz.result(timeout=4000)
    #         except:
    #             sepid_parvaz = []
    #         # --- mehrab
    #         try:
    #             mehrab = mehrab.result(timeout=50000)
    #         except:
    #             mehrab = []
    #         # --- parmis
    #         try:
    #             parmis = parmis.result(timeout=4000)
    #         except:
    #             parmis = []
    #         # --- hamsafar
    #         try:
    #             hamsafar = hamsafar.result(timeout=4000)
    #         except:
    #             hamsafar = []
    #         # --- tak_setareh
    #         try:
    #             tak_setareh = tak_setareh.result(timeout=4000)
    #         except:
    #             tak_setareh = []
    #         # ---
    #         print("--------------------------------")
    #         print("eghamat => ", len(eghamat))
    #         print("moghim => ", len(moghim))
    #         print("shayan_gasht => ", len(shayan_gasht))
    #         print("kimiya => ", len(kimiya))
    #         print("eram2mhd => ", len(eram2mhd))
    #         print("alwin => ", len(alwin))
    #         print("deltaban => ", len(deltaban))
    #         print("booking => ", len(booking))
    #         print("rahbal => ", len(rahbal))
    #         print("hrc => ", len(hrc))
    #         print("dayan => ", len(dayan))
    #         print("omid oj => ", len(omid_oj))
    #         print("sepid parvaz => ", len(sepid_parvaz))
    #         print("mehrab => ", len(mehrab))
    #         print("parmis => ", len(parmis))
    #         print("hamsafar => ", len(hamsafar))
    #         print("tak_setareh => ", len(tak_setareh))
    #         # # # ---
    #         # #
    #         # #
    #         # # #============
    #         # # # Integration (ramin)
    #         # # #=========
    #         # #
    #         #
    #         # #====================
    #         result.extend(eghamat)
    #         result.extend(moghim)
    #         result.extend(eram2mhd)
    #         result.extend(kimiya)
    #         result.extend(shayan_gasht)
    #         result.extend(alwin)
    #         result.extend(deltaban)
    #         result.extend(booking)
    #         result.extend(rahbal)
    #         result.extend(hrc)
    #         result.extend(dayan)
    #         result.extend(omid_oj)
    #         result.extend(sepid_parvaz)
    #         result.extend(mehrab)
    #         result.extend(parmis)
    #         result.extend(hamsafar)
    #         result.extend(tak_setareh)
    #     # ---
    #     return self.ready_data(result, "KIH")
    #
    #
    #
    # def get_gsm_data(self):
    #     result = []
    #     # ---
    #     with ThreadPoolExecutor(max_workers=85) as executor:
    #
    #
    #
    #         #=== Eghamat24========
    #         eghamat = Eghamat24(self.target, self.start_date, self.end_date, self.adults)
    #         eghamat = executor.submit(eghamat.get_result)
    #         #====================
    #
    #         # # --- booking
    #         booking = Booking(self.target, self.start_date, self.end_date, self.adults)
    #         booking = executor.submit(booking.get_result)
    #
    #         # --- TAK_SETAREH
    #         tak_setareh = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,
    #                                   'tak_setareh')
    #         tak_setareh = executor.submit(tak_setareh.get_result)
    #
    #         # # --- rahbal
    #         rahbal = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal')
    #         rahbal = executor.submit(rahbal.get_result)
    #
    #         # --- MEHRAB
    #         mehrab = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab')
    #         mehrab = executor.submit(mehrab.get_result)
    #
    #
    #
    #         # --- alwin
    #         alwin = Alwin(self.target, self.start_date, self.end_date, self.adults)
    #         alwin = executor.submit(alwin.get_result)
    #         # --- IMAN
    #         iman = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, IMAN, 'iman')
    #         iman = executor.submit(iman.get_result)
    #         # --- FLAMINGO
    #         flamingo = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, FLAMINGO, 'flamingo')
    #         flamingo = executor.submit(flamingo.get_result)
    #         # --- SHAYAN GASHT
    #         shayan_gasht = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,
    #                                    'shayan_gasht')
    #         shayan_gasht = executor.submit(shayan_gasht.get_result)
    #         # # --- DOLFIN
    #         dolfin = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DOLFIN, 'dolfin')
    #         dolfin = executor.submit(dolfin.get_result)
    #         # # --- YEGANE FARD
    #         yegane_fard = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, YEGANE_FARD,
    #                                   'yegane_fard')
    #         yegane_fard = executor.submit(yegane_fard.get_result)
    #
    #         # # --- safiran
    #         safiran = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SAFIRAN,
    #                                   'safiran')
    #         safiran = executor.submit(safiran.get_result)
    #
    #         # # --- hamood
    #         hamood = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMOOD,
    #                                   'hamood')
    #         hamood = executor.submit(hamood.get_result)
    #
    #
    #
    #         # --- eghamat
    #         try:
    #             eghamat = eghamat.result(timeout=40)
    #         except:
    #             eghamat = []
    #
    #
    #         # --- tak_setareh
    #         try:
    #             tak_setareh = tak_setareh.result(timeout=40)
    #         except:
    #             tak_setareh = []
    #
    #         # --- rahbal
    #         try:
    #             rahbal = rahbal.result(timeout=40)
    #         except:
    #             rahbal = []
    #
    #         # --- mehrab
    #         try:
    #             mehrab = mehrab.result(timeout=40)
    #         except:
    #             mehrab = []
    #
    #
    #
    #
    #         # --- ALWIN
    #         try:
    #             alwin = alwin.result(timeout=40)
    #         except:
    #             alwin = []
    #         # --- booking
    #         try:
    #             booking = booking.result(timeout=400)
    #         except:
    #             booking = []
    #
    #         # --- IMAN
    #         try:
    #             iman = iman.result(timeout=40)
    #         except:
    #             iman = []
    #         # --- FLAMINGO
    #         try:
    #             flamingo = flamingo.result(timeout=40)
    #         except:
    #             flamingo = []
    #         # --- SHAYAN GASHT
    #         try:
    #             shayan_gasht = shayan_gasht.result(timeout=40)
    #         except:
    #             shayan_gasht = []
    #         # --- DOLFIN
    #         try:
    #             dolfin = dolfin.result(timeout=40)
    #         except:
    #             dolfin = []
    #         # --- YEGANE FARD
    #         try:
    #             yegane_fard = yegane_fard.result(timeout=40)
    #         except:
    #             yegane_fard = []
    #
    #
    #         # --- tak_setareh
    #         try:
    #             safiran = safiran.result(timeout=40)
    #         except:
    #             safiran = []
    #
    #         # --- hamood
    #         try:
    #             hamood = hamood.result(timeout=40)
    #         except:
    #             hamood = []
    #
    #
    #
    #
    #
    #         # ---
    #         print("--------------------------------")
    #         print("eghamat => ", len(eghamat))
    #         print("alwin => ", len(alwin))
    #         print("tak_setareh => ", len(tak_setareh))
    #         print("mehrab => ", len(mehrab))
    #         print("rahbal => ", len(rahbal))
    #         print("booking => ", len(booking))
    #         print("iman => ", len(iman))
    #         print("flamingo => ", len(flamingo))
    #         print("shayan_gasht => ", len(shayan_gasht))
    #         print("dolfin => ", len(dolfin))
    #         print("yegane_fard => ", len(yegane_fard))
    #         print("safiran => ", len(safiran))
    #         print("hamood => ", len(hamood))
    #         # ---
    #         result.extend(eghamat)
    #         result.extend(alwin)
    #         result.extend(tak_setareh)
    #         result.extend(rahbal)
    #         result.extend(mehrab)
    #         result.extend(booking)
    #         result.extend(iman)
    #         result.extend(flamingo)
    #         result.extend(shayan_gasht)
    #         result.extend(dolfin)
    #         result.extend(yegane_fard)
    #         result.extend(safiran)
    #         result.extend(hamood)
    #     # ---
    #     # return self.ready_data(result, "GSM")
    #     return self.read_data_GSM(result)


    #=== koli hazer konid!!!



    # def get_ALLDestination_data_NEW(self):
    #     def execute_service(service_obj):
    #         """Helper function to execute a service and handle timeouts."""
    #         try:
    #             return service_obj.get_result()
    #         except Exception as e:
    #             return []
    #
    #     services = [
    #         # List of service objects
    #         ("Deltaban", Deltaban(self.target, self.start_date, self.end_date, self.adults)),
    #         ("Alwin", Alwin(self.target, self.start_date, self.end_date, self.adults)),
    #         ("Snapp", Snapp(self.target, self.start_date, self.end_date, self.adults)),
    #         ("Alaedin", Alaedin(self.target, self.start_date, self.end_date, self.adults)),
    #         ("Eghamat24", Eghamat24(self.target, self.start_date, self.end_date, self.adults)),
    #         # ("Trivago",Trivago(self.target,self.start_date,self.end_date,self.adults)),
    #         # ("FlyToday", FlyToday(self.target,self.start_date,self.end_date,self.adults)),
    #         # ("Moghim24", Moghim24(self.target, self.start_date, self.end_date, self.adults)),
    #         ("Booking", Booking(self.target, self.start_date, self.end_date, self.adults)),
    #         ("Jimbo", Jimbo(self.target, self.start_date, self.end_date, self.adults)),
    #         # ("SepehrHotel_RAHBAL",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal')),
    #         # ("SepehrHotel_HRC", SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HRC, 'hrc')),
    #         # ("SepehrHotel_DAYAN", SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DAYAN, 'dayan')),
    #         # ("SepehrHotel_OMIDOJ",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, OMID_OJ, 'omid_oj')),
    #         # ("SepehrHotel_SEPIDPARVAZ",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SEPID_PARVAZ,'sepid_parvaz')),
    #         # ("SepehrHotel_PARMIS",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, PARMIS, 'parmis')),
    #         # ("SepehrHotel_MEHRAB",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab')),
    #         # ("SepehrHotel_HAMSAFAR",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMSAFAR, 'hamsafar')),
    #         # ("SepehrHotel_TAKSEAREH",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,'tak_setareh')),
    #         # ("SepehrHotel_KIMIYA",SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TOURISTKISH,'kimiya')),
    #         # ("SepehrHotel_ERAM2MHD", SepehrHotel(self.target, self.start_date, self.end_date, self.adults, ERAM2MHD,'eram2mhd')),
    #         # ("SepehrHotel_SHAYANGASHT",  SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,'shayan_gasht')),
    #         # ("SepehrHotel_IMANZAER",  SepehrHotel(self.target, self.start_date, self.end_date, self.adults, IMAN, 'iman')),
    #         # ("SepehrHotel_FLAMINGO",  SepehrHotel(self.target, self.start_date, self.end_date, self.adults, FLAMINGO, 'flamingo')),
    #         # ("SepehrHotel_YEGANEHFARD",   SepehrHotel(self.target, self.start_date, self.end_date, self.adults, YEGANE_FARD,'yegane_fard')),
    #         # ("SepehrHotel_HAMOOD",   SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMOOD,'hamood')),
    #         # ("SepehrHotel_SAFIRAN",   SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SAFIRAN,'safiran')),
    #         # ("SepehrHotel_DOLFIN",   SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DOLFIN, 'dolfin')),
    #
    #         #
    #     ]
    #
    #     results = []
    #     executor= ThreadPoolExecutor(max_workers=85)
    #     # with ThreadPoolExecutor(max_workers=85) as executor:
    #     # Submit the get_result method for each service
    #     future_to_service = {
    #         executor.submit(service.get_result): name for name, service in services
    #     }
    #
    #     # Wait for exactly 20 seconds, whether tasks complete or not
    #     done, not_done = wait(future_to_service.keys(), timeout=30)
    #
    #     # Collect results from completed futures
    #     for future in done:
    #         service_name = future_to_service[future]
    #         try:
    #             result = future.result(timeout=0)  # No additional waiting
    #             print(f"Service {service_name} successful, length = {len(result)}")
    #             results.extend(result)
    #         except Exception as e:
    #             print(f"Service {service_name} failed with exception: {e}")
    #
    #     # If there are still pending tasks, wait for more time
    #     if not_done:
    #         print(f"Waiting additional time for {len(not_done)} unfinished tasks...")
    #         additional_done, still_not_done = wait(not_done, timeout=30)  # Adjust the timeout as needed
    #
    #         # Process tasks completed during the additional wait
    #         for future in additional_done:
    #             service_name = future_to_service[future]
    #             try:
    #                 result = future.result(timeout=0)  # No additional waiting
    #                 print(f"Service {service_name} successful (after additional wait), length = {len(result)}")
    #                 results.extend(result)
    #             except Exception as e:
    #                 print(f"Service {service_name} failed (after additional wait) with exception: {e}")
    #
    #         # Handle tasks that still didn't complete
    #         for future in still_not_done:
    #             service_name = future_to_service[future]
    #             print(f"Service {service_name} did not complete even after additional wait.")
    #             # Optionally, cancel or handle these pending tasks
    #             future.cancel()
    #     #
    #     # # Handle unfinished threads
    #     # for future in not_done:
    #     #     service_name = future_to_service[future]
    #     #     print(f"Service {service_name} did not complete within 20 seconds.")
    #     #     # Optionally, cancel pending tasks or take other actions
    #     #     future.cancel()
    #
    #
    #
    #     #
    #     # # Collect results as they complete
    #     # for future in as_completed(future_to_service):
    #     #     service_name = future_to_service[future]
    #     #
    #     #     try:
    #     #         result = future.result(timeout=50)  # Adjust timeout as needed
    #     #         print(f"Service {service_name} Successfull    length== {len(result)}")
    #     #         results.extend(result)
    #     #     except Exception as e:
    #     #         print(f"Service {service_name} failed with exception: {e}")
    #
    #
    #
    #     print('Finish Services ..........')
    #     result_read=self.read_data_ALLDestination(results)
    #     return result_read
    #


    def get_ALLDestination_data(self,iter):
        try:
            t1 = datetime.now()
            results = []

            #
            # hotel_tasks = {
            #     "darvishi": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DARVISHI, 'darvishi',self.isAnalysis,self.hotelstarAnalysis),
            #     # "moeindarbari": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MOEINDARBARI,'moeindarbari',self.isAnalysis,self.hotelstarAnalysis),
            #     "deltaban": Deltaban(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis),
            #     # "alwin": Alwin(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis),
            #     "snapp": Snapp(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis),
            #     "alaedin": Alaedin(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis),
            #     "eghamat": Eghamat24(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis),
            #     "booking": Booking(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis),
            #     "jimboo": Jimbo(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis),
            #     # "rahbal": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal',self.isAnalysis,self.hotelstarAnalysis),
            #     # "hrc": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HRC, 'hrc',self.isAnalysis,self.hotelstarAnalysis),
            #     # "dayan": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DAYAN, 'dayan',self.isAnalysis,self.hotelstarAnalysis),
            #     # "omid_oj": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, OMID_OJ, 'omid_oj',self.isAnalysis,self.hotelstarAnalysis),
            #     # "sepid_parvaz": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SEPID_PARVAZ,'sepid_parvaz',self.isAnalysis,self.hotelstarAnalysis),
            #     # "parmis": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, PARMIS, 'parmis',self.isAnalysis,self.hotelstarAnalysis),
            #     # "mehrab": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab',self.isAnalysis,self.hotelstarAnalysis),
            #     # "hamsafar": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMSAFAR, 'hamsafar',self.isAnalysis,self.hotelstarAnalysis),
            #     # "tak_setareh": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,'tak_setareh',self.isAnalysis,self.hotelstarAnalysis),
            #     # "kimiya": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TOURISTKISH, 'kimiya',self.isAnalysis,self.hotelstarAnalysis),
            #     # "eram2mhd": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, ERAM2MHD, 'eram2mhd',self.isAnalysis,self.hotelstarAnalysis),
            #     # "shayan_gasht": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,'shayan_gasht',self.isAnalysis,self.hotelstarAnalysis),
            #     # "iman": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, IMAN, 'iman',self.isAnalysis,self.hotelstarAnalysis),
            #     # "flamingo": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, FLAMINGO, 'flamingo',self.isAnalysis,self.hotelstarAnalysis),
            #     # "yegane_fard": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, YEGANE_FARD,'yegane_fard',self.isAnalysis,self.hotelstarAnalysis),
            #     # "hamood": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMOOD, 'hamood',self.isAnalysis,self.hotelstarAnalysis),
            #     # "safiran": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SAFIRAN, 'safiran',self.isAnalysis,self.hotelstarAnalysis),
            #     # "dolfin": SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DOLFIN, 'dolfin',self.isAnalysis,self.hotelstarAnalysis)
            # }

            hotel_tasks = {
                "deltaban": Deltaban(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp),
                # # # # "alwin": Alwin(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp),
                # "snapp": Snapp(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp),
                "alaedin": Alaedin(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp),
                # "eghamat": Eghamat24(self.target, self.start_date, self.end_date, self.adults,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp),
                # "booking": Booking(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp),
                # "jimboo": Jimbo(self.target, self.start_date, self.end_date, self.adults,iter,self.isAnalysis,self.hotelstarAnalysis,self.priorityTimestamp),
                #
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
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, DARVISHI, 'darvishi', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='darvishi'
                    elif key == 'moeindarbari' and task==1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, MOEINDARBARI, 'moeindarbari', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='moeindarbari'
                    elif key == 'rahbal' and task==1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, RAHBAL, 'rahbal', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='rahbal'
                    elif key == 'hrc' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, HRC, 'hrc', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='hrc'
                    elif key == 'dayan' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, DAYAN, 'dayan', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='dayan'
                    elif key == 'omid_oj' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, OMID_OJ, 'omid_oj', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='omid_oj'
                    elif key == 'hrc' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, HRC, 'hrc', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='hrc'
                    elif key == 'sepid_parvaz' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, SEPID_PARVAZ, 'sepid_parvaz', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='sepid_parvaz'
                    elif key == 'parmis' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, PARMIS, 'parmis', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='parmis'
                    elif key == 'mehrab' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, MEHRAB, 'mehrab', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='mehrab'
                    elif key == 'hamsafar' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, HAMSAFAR, 'hamsafar', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='hamsafar'
                    elif key == 'tak_setareh' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, TAK_SETAREH, 'tak_setareh', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='tak_setareh'
                    elif key == 'kimiya' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, TOURISTKISH, 'kimiya', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='kimiya'
                    elif key == 'eram2mhd' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, ERAM2MHD, 'eram2mhd', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='eram2mhd'
                    elif key == 'shayan_gasht' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, SHAYAN_GASHT, 'shayan_gasht', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='shayan_gasht'

                    elif key == 'iman' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, IMAN, 'iman', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='iman'
                    elif key == 'flamingo' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, FLAMINGO, 'flamingo', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='flamingo'
                    elif key == 'yegane_fard' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, YEGANE_FARD, 'yegane_fard', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='yegane_fard'
                    elif key == 'hamood' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, HAMOOD, 'hamood', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='hamood'
                    elif key == 'safiran' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, SAFIRAN, 'safiran', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='safiran'
                    elif key == 'dolfin' and task == 1:
                        fu[executor.submit(
                            sepehr_get_result, self.target, self.start_date, self.end_date,
                            self.adults, DOLFIN, 'dolfin', self.isAnalysis, self.hotelstarAnalysis,self.priorityTimestamp
                        )]='dolfin'

                        # ??? Complete ??
                    else:
                        fu[executor.submit(task.get_result)]=key

                #--- OLD ---
                # futures = {executor.submit(task.get_result): key for key, task in hotel_tasks.items()}
                # print(f' time Assign tasks --- {(datetime.now() - startTime).total_seconds()} ')
                logger.info(f' time Assign tasks --- {(datetime.now() - startTime).total_seconds()}' )

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

            t1=datetime.now()
            temp=self.read_data_ALLDestination(results)
            # print(f' time read_data_ALLDestination --- {(datetime.now() - t1).total_seconds()} ')
            logger.info(f' time read_data_ALLDestination --- {(datetime.now() - t1).total_seconds()}')

            return temp

        except Exception as e:
            # Log the error and the line number
            print(f"An error occurred: {e}")
            tb = traceback.format_exc()  # Get the full traceback as a string
            print(f"Traceback details:\n{tb}")

            return []


    #
    # def get_ALLDestination_data_old(self):
    #     try:
    #         # #=== read from disk
    #         # import json
    #         #
    #         # fp=open('sorted_hotels_dict.json','r',encoding='utf8')
    #         # aa=fp.read()
    #         # sorted_hotels_dict = json.loads(aa)
    #         # return list(sorted_hotels_dict.values())
    #         # #======
    #
    #
    #
    #         result = []
    #         # ---
    #         with ThreadPoolExecutor(max_workers=85) as executor:
    #             # # #
    #
    #             # #=== Trivago ===
    #             # trivago=Trivago(self.target,self.start_date,self.end_date,self.adults)
    #             # trivago = executor.submit(trivago.get_result)
    #             # #===========
    #
    #             #darvishi
    #             # # --- darvishi
    #             darvishi = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DARVISHI, 'darvishi')
    #             darvishi = executor.submit(darvishi.get_result)
    #
    #             # # --- MoeinDarbari
    #             moeindarbari = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MOEINDARBARI, 'moeindarbari')
    #             moeindarbari = executor.submit(moeindarbari.get_result)
    #
    #
    #
    #
    #             # # # --- deltaban
    #             deltaban = Deltaban(self.target, self.start_date, self.end_date, self.adults)
    #             deltaban = executor.submit(deltaban.get_result)
    #
    #
    #
    #
    #             # # --- alwin
    #             alwin = Alwin(self.target, self.start_date, self.end_date, self.adults)
    #             alwin = executor.submit(alwin.get_result)
    #
    #
    #             #
    #             # #=== snapp ===
    #             snapp=Snapp(self.target,self.start_date,self.end_date,self.adults)
    #             snapp = executor.submit(snapp.get_result)
    #             # #===========
    #             #
    #             # #
    #             #=== Alaedin ===
    #             alaedin=Alaedin(self.target,self.start_date,self.end_date,self.adults)
    #             alaedin = executor.submit(alaedin.get_result)
    #             # #===========
    #             #
    #             # # #=== FlyToday ===
    #             # # flytoday=FlyToday(self.target,self.start_date,self.end_date,self.adults)
    #             # # flytoday = executor.submit(flytoday.get_result)
    #             # # #===========
    #             #
    #             # # #=== Eghamat24========
    #             eghamat = Eghamat24(self.target, self.start_date, self.end_date, self.adults)
    #             eghamat = executor.submit(eghamat.get_result)
    #             # # # ====================
    #             #
    #             #
    #             # # --- moghim24
    #             # moghim = Moghim24(self.target, self.start_date, self.end_date, self.adults)
    #             # moghim = executor.submit(moghim.get_result)
    #             #
    #             #
    #             #
    #             #
    #             #
    #
    #
    #             # # # --- booking
    #             booking = Booking(self.target, self.start_date, self.end_date, self.adults)
    #             booking = executor.submit(booking.get_result)
    #
    #             # # # --- jimboo
    #             jimboo = Jimbo(self.target, self.start_date, self.end_date, self.adults)
    #             jimboo = executor.submit(jimboo.get_result)
    #
    #
    #             # # --- rahbal
    #             rahbal = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal')
    #             rahbal = executor.submit(rahbal.get_result)
    #             # --- HRC
    #             hrc = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HRC, 'hrc')
    #             hrc = executor.submit(hrc.get_result)
    #             # --- DAYAN
    #             dayan = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DAYAN, 'dayan')
    #             dayan = executor.submit(dayan.get_result)
    #             # --- OMID_OJ
    #             omid_oj = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, OMID_OJ, 'omid_oj')
    #             omid_oj = executor.submit(omid_oj.get_result)
    #             # --- SEPID_PARVAZ
    #             sepid_parvaz = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SEPID_PARVAZ,
    #                                        'sepid_parvaz')
    #             sepid_parvaz = executor.submit(sepid_parvaz.get_result)
    #             # --- PARMIS
    #             parmis = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, PARMIS, 'parmis')
    #             parmis = executor.submit(parmis.get_result)
    #             # --- MEHRAB
    #             mehrab = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab')
    #             mehrab = executor.submit(mehrab.get_result)
    #             # --- HAMSAFAR
    #             hamsafar = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMSAFAR, 'hamsafar')
    #             hamsafar = executor.submit(hamsafar.get_result)
    #             # --- TAK_SETAREH
    #             tak_setareh = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,
    #                                       'tak_setareh')
    #             tak_setareh = executor.submit(tak_setareh.get_result)
    #
    #             # --- Kimiya
    #             kimiya = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TOURISTKISH,
    #                                       'kimiya')
    #             kimiya = executor.submit(kimiya.get_result)
    #
    #             # --- Eram
    #             eram2mhd = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, ERAM2MHD,
    #                                       'eram2mhd')
    #             eram2mhd = executor.submit(eram2mhd.get_result)
    #
    #             # --- SHAYAN GASHT
    #             shayan_gasht = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,
    #                                        'shayan_gasht')
    #             shayan_gasht = executor.submit(shayan_gasht.get_result)
    #
    #             # --- IMAN
    #             iman = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, IMAN, 'iman')
    #             iman = executor.submit(iman.get_result)
    #             # --- FLAMINGO
    #             flamingo = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, FLAMINGO, 'flamingo')
    #             flamingo = executor.submit(flamingo.get_result)
    #
    #             # # --- YEGANE FARD
    #             yegane_fard = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, YEGANE_FARD,
    #                                       'yegane_fard')
    #             yegane_fard = executor.submit(yegane_fard.get_result)
    #
    #             # # --- hamood
    #             hamood = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMOOD,'hamood')
    #             hamood = executor.submit(hamood.get_result)
    #
    #             # # --- safiran
    #             safiran = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SAFIRAN,
    #                                   'safiran')
    #             safiran = executor.submit(safiran.get_result)
    #
    #             # # --- DOLFIN
    #             dolfin = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DOLFIN, 'dolfin')
    #             dolfin = executor.submit(dolfin.get_result)
    #
    #             # # --- trivago
    #             # try:
    #             #     trivago = trivago.result(timeout=10000)
    #             # except:
    #             #     trivago = []
    #             #
    #
    #             # # --- snapp
    #             try:
    #                 snapp = snapp.result(timeout=1000000)
    #             except:
    #                 snapp = []
    #             #
    #             # # # --- ALAEDIN
    #             try:
    #                 alaedin = alaedin.result(timeout=1000000)
    #             except:
    #                 alaedin = []
    #
    #             # #--- FlyToday
    #             # try:
    #             #     flytoday=flytoday.result(timeout=10000)
    #             # except:
    #             #     flytoday=[]
    #
    #
    #             #
    #             # #--- moeindarbari
    #             try:
    #                 moeindarbari=moeindarbari.result(timeout=100000)
    #             except:
    #                 moeindarbari=[]
    #
    #             # #--- darvishi
    #             try:
    #                 darvishi=darvishi.result(timeout=100000)
    #             except:
    #                 darvishi=[]
    #
    #             #
    #             # #--- eghamat24
    #             try:
    #                 eghamat=eghamat.result(timeout=100000)
    #             except:
    #                 eghamat=[]
    #             # # eghamat = []
    #             #
    #             #
    #             # #--- moghim24
    #             try:
    #                 kimiya=kimiya.result(timeout=1000)
    #             except:
    #                 kimiya=[]
    #
    #             try:
    #                 eram2mhd=eram2mhd.result(timeout=1000)
    #             except:
    #                 eram2mhd=[]
    #
    #
    #             try:
    #                 shayan_gasht=shayan_gasht.result(timeout=1000)
    #             except:
    #                 shayan_gasht=[]
    #
    #             # #--- moghim24
    #             # try:
    #             #     moghim=moghim.result(timeout=1000)
    #             # except:
    #             #     moghim=[]
    #
    #             #
    #             # --- deltaban
    #             try:
    #                 deltaban = deltaban.result(timeout=60)
    #             except:
    #                 deltaban = []
    #
    #             # deltaban = []
    #             # # # --- alwin
    #             try:
    #                 alwin = alwin.result(timeout=400000)
    #             except:
    #                 alwin = []
    #             # alwin = []
    #
    #             # # --- booking
    #             try:
    #                 booking = booking.result(timeout=400000)
    #             except:
    #                 booking = []
    #
    #             # # --- jimboo
    #             try:
    #                 jimboo = jimboo.result(timeout=400000)
    #             except:
    #                 jimboo = []
    #
    #
    #             # --- rahbal
    #             try:
    #                 rahbal = rahbal.result(timeout=4000)
    #             except:
    #                 rahbal = []
    #             # --- hrc
    #             try:
    #                 hrc = hrc.result(timeout=40)
    #             except:
    #                 hrc = []
    #             # --- dayan
    #             try:
    #                 dayan = dayan.result(timeout=4000)
    #             except:
    #                 dayan = []
    #             # --- omid_oj
    #             try:
    #                 omid_oj = omid_oj.result(timeout=4000)
    #             except:
    #                 omid_oj = []
    #             # --- sepid_parvaz
    #             try:
    #                 sepid_parvaz = sepid_parvaz.result(timeout=4000)
    #             except:
    #                 sepid_parvaz = []
    #             # --- mehrab
    #             try:
    #                 mehrab = mehrab.result(timeout=50000)
    #             except:
    #                 mehrab = []
    #             # --- parmis
    #             try:
    #                 parmis = parmis.result(timeout=4000)
    #             except:
    #                 parmis = []
    #             # --- hamsafar
    #             try:
    #                 hamsafar = hamsafar.result(timeout=4000)
    #             except:
    #                 hamsafar = []
    #             # --- tak_setareh
    #             try:
    #                 tak_setareh = tak_setareh.result(timeout=4000)
    #             except:
    #                 tak_setareh = []
    #
    #             # --- hamood
    #             try:
    #                 hamood = hamood.result(timeout=40)
    #             except:
    #                 hamood = []
    #
    #                 # --- YEGANE FARD
    #             try:
    #                 yegane_fard = yegane_fard.result(timeout=40)
    #             except:
    #                 yegane_fard = []
    #
    #                 # --- FLAMINGO
    #             try:
    #                 flamingo = flamingo.result(timeout=40)
    #             except:
    #                 flamingo = []
    #
    #             # --- IMAN
    #             try:
    #                 iman = iman.result(timeout=40)
    #             except:
    #                 iman = []
    #
    #             try:
    #                 safiran = safiran.result(timeout=40)
    #             except:
    #                 safiran = []
    #
    #             # --- DOLFIN
    #             try:
    #                 dolfin = dolfin.result(timeout=40)
    #             except:
    #                 dolfin = []
    #
    #             # ---
    #             # print("--------------------------------")
    #             # print("trivago => ", len(trivago))
    #             print("alaedin => ", len(alaedin))
    #
    #             print("moeindarbari => ", len(moeindarbari))
    #             print("darvishi => ", len(darvishi))
    #
    #
    #             print("snapp => ", len(snapp))
    #             # print("flytoday => ", len(flytoday))
    #             print("eghamat => ", len(eghamat))
    #             # print("moghim => ", len(moghim))
    #             print("shayan_gasht => ", len(shayan_gasht))
    #             print("kimiya => ", len(kimiya))
    #             print("eram2mhd => ", len(eram2mhd))
    #             print("alwin => ", len(alwin))
    #             print("deltaban => ", len(deltaban))
    #             print("booking => ", len(booking))
    #             print("jimboo => ", len(jimboo))
    #             print("rahbal => ", len(rahbal))
    #             print("hrc => ", len(hrc))
    #             print("dayan => ", len(dayan))
    #             print("omid oj => ", len(omid_oj))
    #             print("sepid parvaz => ", len(sepid_parvaz))
    #             print("mehrab => ", len(mehrab))
    #             print("parmis => ", len(parmis))
    #             print("hamsafar => ", len(hamsafar))
    #             print("tak_setareh => ", len(tak_setareh))
    #
    #
    #             print("dolfin => ", len(dolfin))
    #             print("yegane_fard => ", len(yegane_fard))
    #             print("safiran => ", len(safiran))
    #             print("hamood => ", len(hamood))
    #             print("iman => ", len(iman))
    #             print("flamingo => ", len(flamingo))
    #
    #
    #             # # # ---
    #             # #
    #             # #
    #             # # #============
    #             # # # Integration (ramin)
    #             # # #=========
    #             # #
    #             #
    #             # #====================
    #             # # result.extend(trivago)
    #             result.extend(moeindarbari)
    #             result.extend(darvishi)
    #
    #             result.extend(alaedin)
    #
    #             result.extend(snapp)
    #             # # result.extend(flytoday)
    #             result.extend(eghamat)
    #             # # # result.extend(moghim)
    #             result.extend(eram2mhd)
    #             result.extend(kimiya)
    #             result.extend(shayan_gasht)
    #             result.extend(alwin)
    #             result.extend(deltaban)
    #             result.extend(booking)
    #             result.extend(jimboo)
    #             result.extend(rahbal)
    #             result.extend(hrc)
    #             result.extend(dayan)
    #             result.extend(omid_oj)
    #             result.extend(sepid_parvaz)
    #             result.extend(mehrab)
    #             result.extend(parmis)
    #             result.extend(hamsafar)
    #             result.extend(tak_setareh)
    #
    #             result.extend(dolfin)
    #             result.extend(yegane_fard)
    #             result.extend(safiran)
    #             result.extend(hamood)
    #             result.extend(iman)
    #             result.extend(flamingo)
    #
    #
    #
    #
    #
    #         # ---
    #
    #         # # # # #--- Save result as Json
    #         # import json
    #         # jsonData=json.dumps(result)
    #         # fp=open(f'{self.target}__jsondata_NEWWWWWW_mehrab.json','w',encoding='utf8')
    #         # fp.write(jsonData)
    #         # fp.close()
    #         # # # #----------
    #
    #
    #     except Exception as e:
    #         # Log the error and the line number
    #         print(f"An error occurred: {e}")
    #         tb = traceback.format_exc()  # Get the full traceback as a string
    #         print(f"Traceback details:\n{tb}")
    #
    #     return self.read_data_ALLDestination(result)
    #

    #====


    def get_result(self,iter):


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

        # #----- read --
        # import json
        # try:
        #     with open('result.json', 'r', encoding='utf8') as fp:
        #         result = json.load(fp)
        #
        #     return result
        # except:
        #     ''
        #
        # #---------
        redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}"
        if self.use_cache and check_redis_key(redis_key):
            return get_dict_to_redis(redis_key)
        else:
            # if self.target == "KIH":
            #     result = self.get_kih_data()
            # elif self.target == "GSM":
            #     result = self.get_gsm_data()
            # else:
            #     result=self.get_ALLDestination_data()

            #
            # #=============
            # #== Check is Redundant process or Not?
            # #=============
            # redis_key_redundant = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}_Doing"
            # if check_redis_key(redis_key_redundant):
            #     print( f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}_Doing")
            #     #== wait until result get readu ...
            #     iter=10
            #     while(True):
            #         try:
            #             if check_redis_key(redis_key):
            #                 return get_dict_to_redis(redis_key)
            #             else:
            #                 iter=iter-1
            #                 time.sleep(20)
            #
            #             if (iter==0):
            #                 return []
            #         except:
            #             return []
            #
            #
            #
            # else:  # First time
            #     add_dict_to_redis(redis_key_redundant,'1',180)   # add doing in redis
            #     result = self.get_ALLDestination_data()


            result = self.get_ALLDestination_data(iter)
            #== Multi Thread ===
            print('start caching ..........')
            if len(result):
                with ThreadPoolExecutor(max_workers=100) as executorr:
                    executorr.submit(add_dict_to_redis, redis_key, result, self.redis_expire)  # bayad doing ha delete shavad!! (OK)
            #=====
            #

            return result
