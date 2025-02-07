from datetime import (datetime, timedelta)
from app_crawl.kih.alwin import Alwin24
from app_crawl.kih.booking_api import Booking
from app_crawl.kih.deltaban import Deltaban
from app_crawl.kih.jimbo_api import Jimbo
from app_crawl.ready_tour.sepehr import Sepehr
from app_crawl.cookie import cookie_data
from app_crawl.kih.data import hotels
from app_crawl.helpers import (ready_sepehr_hotel_name, )
from operator import itemgetter
from concurrent.futures import ThreadPoolExecutor,as_completed
from app_crawl.cache.cache import has_key_cache, get_cache, add_cache
from concurrent.futures import as_completed
from datetime import datetime
class TourCollector:
    def __init__(self, source,target,start_date, night_count, hotel_star, adults=2):
        self.start_date = start_date
        try:
            self.end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=int(night_count))
            self.night_count = int(night_count)
        except:
            self.end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=3)
            self.night_count = night_count
        self.hotel_star = hotel_star
        self.executor = ThreadPoolExecutor(max_workers=100)
        self.executor_analysis=ThreadPoolExecutor(max_workers=100)
        self.adults = adults
        self.source=source
        self.target=target

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
            # ---
            if (self.target=="KIH"):
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
                # ---
            # if ("پانیذ" in appended_data['hotel_name']):
            #     print('asdasd')
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



    def get_single_data(self, source, target, start_date, use_cache,iter):
        print(f"Processing data for date: {start_date}")
        print("-" * 40)
        # AJABA
        # Initialize all instances
        providers = [
            ("Booking", Booking(source, target, start_date, self.night_count, adults=self.adults,iter=iter)),
            ("Jimbo", Jimbo(source, target, start_date, self.night_count, adults=self.adults,iter=iter)),
            ("Deltaban", Deltaban(start_date, self.night_count, source, target, adults=self.adults)),

            ("Dayan",Sepehr(source, target, start_date, self.night_count, cookie_data.DAYAN, "dayan", adults=self.adults)),
            ("Sepid Parvaz",Sepehr(source, target, start_date, self.night_count, cookie_data.SEPID_PARVAZ, "sepid_parvaz",adults=self.adults)),
            ("Mehrab Seir",Sepehr(source, target, start_date, self.night_count, cookie_data.MEHRAB, "mehrab", adults=self.adults)),
            ("Rahbal",Sepehr(source, target, start_date, self.night_count, cookie_data.RAHBAL, "rahbal", adults=self.adults)),
            ("Tak Setare", Sepehr(source, target, start_date, self.night_count, cookie_data.TAK_SETAREH, "tak_setare",adults=self.adults)),
            ("Omid Oj",Sepehr(source, target, start_date, self.night_count, cookie_data.OMID_OJ, "omid_oj", adults=self.adults)),
            ("Parmis", Sepehr(source, target, start_date, self.night_count, cookie_data.PARMIS, "parmis", self.adults)),
            ("HRC", Sepehr(source, target, start_date, self.night_count, cookie_data.HRC, "hrc", self.adults)),
            ("Kimiya", Sepehr(source, target, start_date, self.night_count, cookie_data.TOURISTKISH, "kimiya", self.adults)),
            ("Eram2MHD",Sepehr(source, target, start_date, self.night_count, cookie_data.ERAM2MHD, "eram2mhd", self.adults)),
            ("Safiran",Sepehr(source, target, start_date, self.night_count, cookie_data.SAFIRAN, "safiran", self.adults)),
            ("Hamood", Sepehr(source, target, start_date, self.night_count, cookie_data.HAMOOD, "hamood", self.adults)),
            ("Darvishi", Sepehr(source, target, start_date, self.night_count, cookie_data.DARVISHI, "darvishi", self.adults)),
            ("Moeindarbari",Sepehr(source, target, start_date, self.night_count, cookie_data.MOEINDARBARI, "moeindarbari",self.adults)),
        ]

        # Submit tasks to executor
        tasks = {self.executor.submit(instance.get_result): name for name, instance in providers}

        results = []
        provider_status = {}
        startTime=datetime.now()
        # Process tasks as they complete
        for future in as_completed(tasks):
            name = tasks[future]
            try:
                result = future.result(timeout=600)  # Adjust timeout as needed
                results.extend(result.get('data', []))
                spendTime=(datetime.now()-startTime).total_seconds()
                print(f'{name} ----- > spend:  {spendTime}')

                provider_status[name] = {"length": len(result.get('data', [])), "message": result.get('message', '')}
            except Exception as e:
                print(f"{name} failed: {str(e)}")
                provider_status[name] = {"length": 0, "message": "Timeout/Error"}

        # Log results
        for provider, status in provider_status.items():
            print(f"{provider}: {status}")


        return {'data': results, "providers": provider_status}


    def get_single_data_OLD(self, source, target,start_date,use_cache):
        # ---
        result = []
        print("--------------------------------")
        print(start_date)
        print("--------------------------------")
        print("alwin start")

        #alwin_instance = Alwin24(start_date, self.night_count, adults=self.adults) #
        # alwin = self.executor.submit(alwin_instance.get_result)
        #alwin = self.executor.submit(alwin_instance.get_with_selenium,use_cache)

        # source, target="MHD","KIH"
        print("--------------------------------")
        print("booking start")
        booking_instance = Booking(source,target,start_date, self.night_count, adults=self.adults)
        booking = self.executor.submit(booking_instance.get_result)

        print("Jimboo start")
        jimbo_instance = Jimbo(source, target, start_date, self.night_count, adults=self.adults)
        jimbo = self.executor.submit(jimbo_instance.get_result)


        print("--------------------------------")
        print("dayan start")
        dayan_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.DAYAN, "dayan", adults=self.adults)
        dayan = self.executor.submit(dayan_instance.get_result)
        print("--------------------------------")
        print("deltaban start")
        deltaban_instance = Deltaban(start_date, self.night_count,source, target, adults=self.adults)
        deltaban = self.executor.submit(deltaban_instance.get_result)
        print("--------------------------------")
        print("sepid parvaz start")
        sepid_parvaz_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.SEPID_PARVAZ, "sepid_parvaz",
                                       adults=self.adults)
        sepid_parvaz = self.executor.submit(sepid_parvaz_instance.get_result)
        print("--------------------------------")
        print("mehrab seir start")
        mehrab_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.MEHRAB, "mehrab", adults=self.adults)
        mehrab = self.executor.submit(mehrab_instance.get_result)
        print("--------------------------------")
        print("rahbal start")
        rahbal_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.RAHBAL, "rahbal", adults=self.adults)
        rahbal = self.executor.submit(rahbal_instance.get_result)
        print("--------------------------------")
        print("tak setare start")
        tak_setare_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.TAK_SETAREH, "tak_setare",
                                     adults=self.adults)
        tak_setare = self.executor.submit(tak_setare_instance.get_result)
        print("--------------------------------")
        print("omid oj start")
        omid_oj_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.OMID_OJ, "omid_oj",
                                  adults=self.adults)
        omid_oj = self.executor.submit(omid_oj_instance.get_result)

        print("--------------------------------")
        print("parmis start")
        parmis_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.PARMIS, "parmis", self.adults)
        parmis = self.executor.submit(parmis_instance.get_result)

        print("--------------------------------")
        print("HRC")
        HRC_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.HRC, "hrc", self.adults)
        HRC = self.executor.submit(HRC_instance.get_result)

        print("--------------------------------")
        print("--------------------------------")
        print("kimiya")
        kimiya_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.TOURISTKISH, "kimiya", self.adults)
        kimiya = self.executor.submit(kimiya_instance.get_result)

        print("--------------------------------")
        print("eram2mhd")
        eram2mhd_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.ERAM2MHD, "eram2mhd", self.adults)
        eram2mhd = self.executor.submit(eram2mhd_instance.get_result)

        print("--------------------------------")
        print("safiran")
        safiran_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.SAFIRAN, "safiran",
                                   self.adults)
        safiran = self.executor.submit(safiran_instance.get_result)

        print("--------------------------------")
        print("hamood")
        hamood_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.HAMOOD, "hamood",
                                   self.adults)
        hamood = self.executor.submit(hamood_instance.get_result)


        print("--------------------------------")
        print("darvishi")
        darvishi_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.DARVISHI, "darvishi",
                                   self.adults)
        darvishi = self.executor.submit(darvishi_instance.get_result)


        print("--------------------------------")
        print("moeindarbari")
        moeindarbari_instance = Sepehr(source, target, start_date, self.night_count, cookie_data.MOEINDARBARI, "moeindarbari",
                                   self.adults)
        moeindarbari = self.executor.submit(moeindarbari_instance.get_result)



        # ---

        try:
            deltaban = deltaban.result(timeout=400000)
        except TimeoutError as e:
            print("--------------------------------")
            print("deltaban time out", e)
            deltaban = {'status': False, 'data': [], 'message': "تاخیر"}
        # # ---


        try:
            booking = booking.result(timeout=6000)
        except TimeoutError as e:
            print("--------------------------------")
            print("booking time out", e)
            booking = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---

        try:
            jimbo = jimbo.result(timeout=6000)
        except TimeoutError as e:
            print("--------------------------------")
            print("jimbo time out", e)
            jimbo = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---





        # ---
        try:
            dayan = dayan.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("dayan time out", e)
            dayan = {'status': False, 'data': [], 'message': "خطای سیستم"}
        # ---
        try:
            sepid_parvaz = sepid_parvaz.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("sepid_parvaz time out", e)
            sepid_parvaz = {'status': False, 'data': [], 'message': "خطای سیستم"}
        # ---
        try:
            rahbal = rahbal.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("rahbal time out", e)
            rahbal = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---
        try:
            mehrab = mehrab.result(timeout=50000)
        except TimeoutError as e:
            print("--------------------------------")
            print("mehrab time out", e)
            mehrab = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---

        #try:
            #alwin = alwin.result(timeout=1000000)
            # alwin = {'status': False, 'data': [], 'message': "خیر"}
        #except TimeoutError as e:
            #print("--------------------------------")
            #print("alwin time out", e)
            #alwin = {'status': False, 'data': [], 'message': "تاخیر"}

        try:
            tak_setare = tak_setare.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("tak setare time out", e)
            tak_setare = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---
        try:
            omid_oj = omid_oj.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("omid oj time out", e)
            omid_oj = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---
        try:
            parmis = parmis.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("parmis time out", e)
            parmis = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---


        try:
            HRC = HRC.result(timeout=4000)
        except TimeoutError as e:
            print("--------------------------------")
            print("HRC time out", e)
            HRC = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---

        # # ---
        try:
            kimiya = kimiya.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("kimiya time out", e)
            kimiya = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---
        # ---
        try:
            eram2mhd = eram2mhd.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("eram2mhd time out", e)
            eram2mhd = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---
        # ---
        try:
            safiran = safiran.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("safiran time out", e)
            safiran = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---
        # ---
        try:
            hamood = hamood.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("hamood time out", e)
            hamood = {'status': False, 'data': [], 'message': "تاخیر"}
        # ---

        try:
            darvishi = darvishi.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("darvishi time out", e)
            darvishi = {'status': False, 'data': [], 'message': "تاخیر"}

        try:
            moeindarbari = moeindarbari.result(timeout=400)
        except TimeoutError as e:
            print("--------------------------------")
            print("moeindarbari time out", e)
            moeindarbari = {'status': False, 'data': [], 'message': "تاخیر"}

        # ---





        providers = {}
        # ---
        #if isinstance(alwin, dict):
            #result.extend(alwin['data'])
            #providers['alwin'] = {
                #"length": len(alwin['data']),
               # "message": alwin['message'],
               # "url": "https://allwin24.ir/"
            #}
        if isinstance(dayan, dict):
            result.extend(dayan['data'])
            providers['dayan'] = {
                "length": len(dayan['data']),
                "message": dayan['message'],
                "url": f"https://{cookie_data.DAYAN['domain']}"
            }
        if isinstance(deltaban, dict):
            result.extend(deltaban['data'])
            providers['deltaban'] = {
                "length": len(deltaban['data']),
                "message": deltaban['message'],
                "url": 'https://3click.com/'
            }
        if isinstance(sepid_parvaz, dict):
            result.extend(sepid_parvaz['data'])
            providers['sepid_parvaz'] = {
                "length": len(sepid_parvaz['data']),
                "message": sepid_parvaz['message'],
                "url": f"https://{cookie_data.SEPID_PARVAZ['domain']}"
            }
        if isinstance(rahbal, dict):
            result.extend(rahbal['data'])
            providers['rahbal'] = {
                "length": len(rahbal['data']),
                "message": rahbal['message'],
                "url": f"https://{cookie_data.RAHBAL['domain']}"
            }
        if isinstance(mehrab, dict):
            result.extend(mehrab['data'])
            providers['mehrab'] = {
                "length": len(mehrab['data']),
                "message": mehrab['message'],
                "url": f"https://{cookie_data.MEHRAB['domain']}"
            }
        if isinstance(booking, dict):
            result.extend(booking['data'])
            providers['booking'] = {
                "length": len(booking['data']),
                "message": booking['message'],
                "url": "https://www.booking.ir/"
            }

        if isinstance(jimbo, dict):
            result.extend(jimbo['data'])
            providers['Jimboo'] = {
                "length": len(jimbo['data']),
                "message": jimbo['message'],
                "url": "https://www.jimbo.ir/"
            }



        if isinstance(tak_setare, dict):
            result.extend(tak_setare['data'])
            providers['tak_setare'] = {
                "length": len(tak_setare['data']),
                "message": tak_setare['message'],
                "url": f"https://{cookie_data.TAK_SETAREH['domain']}"
            }
        if isinstance(omid_oj, dict):
            result.extend(omid_oj['data'])
            providers['omid_oj'] = {
                "length": len(omid_oj['data']),
                "message": omid_oj['message'],
                "url": f"https://{cookie_data.OMID_OJ['domain']}"
            }
        if isinstance(parmis, dict):
            result.extend(parmis['data'])
            providers['parmis'] = {
                "length": len(parmis['data']),
                "message": parmis['message'],
                "url": f"https://{cookie_data.PARMIS['domain']}"
            }

        if isinstance(HRC, dict):
            result.extend(HRC['data'])
            providers['hrc'] = {
                "length": len(HRC['data']),
                "message": HRC['message'],
                "url": f"https://{cookie_data.HRC['domain']}"
            }
        if isinstance(kimiya, dict):
            result.extend(kimiya['data'])
            providers['kimiya'] = {
                "length": len(kimiya['data']),
                "message": kimiya['message'],
                "url": f"https://{cookie_data.TOURISTKISH['domain']}"
            }
        if isinstance(eram2mhd, dict):
            result.extend(eram2mhd['data'])
            providers['eram2mhd'] = {
                "length": len(eram2mhd['data']),
                "message": eram2mhd['message'],
                "url": f"https://{cookie_data.ERAM2MHD['domain']}"
            }
        if isinstance(hamood, dict):
            result.extend(hamood['data'])
            providers['hamood'] = {
                "length": len(hamood['data']),
                "message": hamood['message'],
                "url": f"https://{cookie_data.HAMOOD['domain']}"
            }
        if isinstance(darvishi, dict):
            result.extend(darvishi['data'])
            providers['darvishi'] = {
                "length": len(darvishi['data']),
                "message": darvishi['message'],
                "url": f"https://{cookie_data.DARVISHI['domain']}"
            }
        if isinstance(moeindarbari, dict):
            result.extend(moeindarbari['data'])
            providers['moeindarbari'] = {
                "length": len(moeindarbari['data']),
                "message": moeindarbari['message'],
                "url": f"https://{cookie_data.MOEINDARBARI['domain']}"
            }


        if isinstance(safiran, dict):
            result.extend(safiran['data'])
            providers['safiran'] = {
                "length": len(safiran['data']),
                "message": safiran['message'],
                "url": f"https://{cookie_data.SAFIRAN['domain']}"
            }

        # ---
        # print("--------------------------------")
        # log = ', '.split([f'{k} => {v["length"]}' for k, v in providers.items()])
        print(f"{start_date} done => {providers}")
        return {'data': result, "providers": providers}


    def get_single_result(self, source, target,start_date=None, show_providers=False, use_cache=True,iter=1):
        if start_date:
            start_date = start_date
        else:
            start_date = self.start_date

        # ???????????? ========= Key ==> Source,target,Startdate ???????????????
        # ++++++++++++++++++++++++++++++++++++++++++
        # # --- redis (can rollback)
        # redis_key = f"ready_{start_date}_{self.night_count}_{self.adults}"
        redis_key = f"ready_{source}_{target}_{start_date}_{self.night_count}_{self.adults}"
        if use_cache and has_key_cache(key=redis_key):
            data = get_cache(key=redis_key, get_time=True)
            if show_providers:
                return data
            else:
                return data['data']
        # --------------------
        #++++++++++++++++++++++++++++++++++++++++++


        data = self.get_single_data(source, target,start_date,use_cache,iter)
        result = self.get_result(data['data'])
        # ---
        #print('Statit Caching....')
        add_cache(key=redis_key, data={'data': result, 'providers': data['providers']})
        #print('End Caching....')
        if show_providers:
            return {'data': result, 'providers': data['providers']}
        else:
            return result

    def get_analysis(self,source, target, range_number: int, use_cache=True):

        # range_number=7
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        date_range = [(start_date + timedelta(days=date)).strftime("%Y-%m-%d") for date in range(range_number)]
        # ---

        # sami_result = self.executor.map(self.get_single_result, date_range)

        #===instead ====
        # futures = [self.executor_analysis.submit(self.get_single_result,source, target, date,False,True) for date in date_range]
        futures = [
            self.executor_analysis.submit(self.get_single_result, source, target, date, False, True, iter)
            for iter, date in enumerate(date_range)
        ]




        sami_result = []
        s_t=datetime.now()
        for future in as_completed(futures):
            try:
                result = future.result()  # This will block until the future is done

                print(f'future_completed in {(datetime.now()-s_t).total_seconds()}')
                sami_result.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")

        #+================

        #
        # result = {date_range[index]: r for index, r in enumerate(sami_result)}
        # sami_result = [
        #     self.get_single_result(start_date=dr, show_providers=False, use_cache=use_cache) for dr in date_range
        # ]
        result = {date_range[index]: r for index, r in enumerate(sami_result)}
        # add_dict_to_redis(redis_key, {'status': True, "data": result}, default_redis_expire)
        return {'status': True, "data": result}
