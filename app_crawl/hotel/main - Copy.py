from .Crawl_Alaedin_ALL_OK import Alaedin
from .DNS_utls import DNS_mapping
from .Hotel_flytoday import FlyToday
from .deltaban import Deltaban
from .booking import Booking
from .alwin import Alwin24
from .moghim24 import Moghim24
from .eghamat24 import Eghamat24
from app_crawl.helpers import (add_dict_to_redis, get_dict_to_redis, check_redis_key, ready_sepehr_gsm_hotel_name,
                               ready_sepehr_hotel_name)
from app_crawl.gsm.data import hotels_GSM
from concurrent.futures import ThreadPoolExecutor
from app_crawl.hotel.sepehr import SepehrHotel
from app_crawl.cookie.cookie_data import (RAHBAL, HRC, DAYAN, OMID_OJ, SEPID_PARVAZ, PARMIS, HAMSAFAR, MEHRAB,
                                          TAK_SETAREH, IMAN, FLAMINGO, SHAYAN_GASHT, DOLFIN, YEGANE_FARD,ERAM2MHD,TOURISTKISH,SAFIRAN,HAMOOD)
from app_crawl.kih.data import hotels


class Hotel:
    def __init__(self, source, target, start_date, end_date, adults):
        self.source = source
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.redis_expire = 0  # 3 minutes

    def read_data_ALLDestination(self,data):
        ds = DNS_mapping()
        result = {}
        for hotel in data:
            try:

                if (hotel['provider']=='deltaban'):
                    print('asd')
                #=
                hotelname,hotelStar=ds.check_hotelName(hotel['hotel_name'], self.target)
                # ---
                default_data = {
                    "hotel_name":  hotelname,
                    "hotel_star": hotelStar,
                    "min_price": hotel['min_price'],
                    "rooms": [],
                    "provider": hotel['provider']
                }

                if default_data['hotel_name']=='':
                    continue

                # ---
                hotel_name = default_data['hotel_name']
                if hotel_name not in result.keys():
                    result[hotel_name] = default_data
                else:
                    for room in hotel['rooms']:
                        result[hotel_name]['rooms'].append(room)
                    print('tekrari')
                # ---
                if hotel['min_price'] < result[hotel_name]['min_price']:
                    result[hotel_name]['min_price'] = hotel['min_price']
                # ---
                for room in hotel['rooms']:
                    result[hotel_name]['rooms'].append(room)
                # ---
            except:
                continue
        return list(result.values())





    def read_data_GSM(self,data):
        ds = DNS_mapping()
        result = {}
        for hotel in data:

            try:
                # hotel_name = ready_sepehr_gsm_hotel_name(hotel['hotel_name'])
                # ---
                default_data = {
                    "hotel_name":  ds.check_hotelName(hotel['hotel_name'],'GSM'),
                    "hotel_star": hotel['hotel_star'],
                    "min_price": hotel['min_price'],
                    "rooms": [],
                    "provider": hotel['provider']
                }
                # ---
                # found = 0
                # #=== Read DNS ===
                # hotels_DNS=hotels_GSM
                # #========
                #
                # for key, value in hotels_DNS.items():
                #     try:
                #         system_provider = value[hotel['provider']]
                #     except:
                #         # === Default DNS
                #         system_provider = key.replace('هتل', '').replace('کیش', '').strip()
                #         # ====
                #         # continue
                #
                #     if system_provider:
                #         if system_provider.strip() in hotel_name:
                #             default_data['hotel_name'] = key
                #             default_data['hotel_star'] = value['hotel_star']
                #             found = 1
                #
                # #-----
                # if found == 0:  # chizi peyda nashod
                #     continue
                if default_data['hotel_name']=='':
                    continue

                # ---
                hotel_name = default_data['hotel_name']
                if hotel_name not in result.keys():
                    result[hotel_name] = default_data
                # ---
                if hotel['min_price'] < result[hotel_name]['min_price']:
                    result[hotel_name]['min_price'] = hotel['min_price']
                # ---
                for room in hotel['rooms']:
                    result[hotel_name]['rooms'].append(room)
                # ---
                # for key, value in hotels.items():
                #     system_provider = value[hotel['provider']]
                #     if system_provider:
                #         if system_provider.strip() in hotel_name:
                #             default_data['hotel_name'] = key
                #             default_data['hotel_star'] = value['hotel_star']
            except:
                continue
        return list(result.values())



    def ready_data(self,data, target):



        result = {}
        for hotel in data:

            try:
                # ----
                if target == "GSM":
                    hotel_name = ready_sepehr_gsm_hotel_name(hotel['hotel_name'])
                elif target == "KIH":
                    hotel_name = ready_sepehr_hotel_name(hotel['hotel_name'])
                else:
                    return []
                # ---
                default_data = {
                    "hotel_name": hotel_name,
                    "hotel_star": hotel['hotel_star'],
                    "min_price": hotel['min_price'],
                    "rooms": [],
                    "provider": hotel['provider']
                }
                # ---
                found = 0
                #=== Read DNS ===
                # kih -->data.py
                # gsm -> ??????
                #==========
                hotels_DNS=hotels
                if (target=="GSM"):
                    hotels_DNS=hotels_GSM
                #========

                for key, value in hotels_DNS.items():
                    try:
                        system_provider = value[hotel['provider']]
                    except:
                        # === Default DNS
                        system_provider = key.replace('هتل', '').replace('کیش', '').strip()
                        # ====
                        # continue

                    if system_provider:
                        if system_provider.strip() in hotel_name:
                            default_data['hotel_name'] = key
                            default_data['hotel_star'] = value['hotel_star']
                            found = 1

                #-----
                if found == 0:  # chizi peyda nashod
                    continue

                # ---
                hotel_name = default_data['hotel_name']
                if hotel_name not in result.keys():
                    result[hotel_name] = default_data
                # ---
                if hotel['min_price'] < result[hotel_name]['min_price']:
                    result[hotel_name]['min_price'] = hotel['min_price']
                # ---
                for room in hotel['rooms']:
                    result[hotel_name]['rooms'].append(room)
                # ---
                # for key, value in hotels.items():
                #     system_provider = value[hotel['provider']]
                #     if system_provider:
                #         if system_provider.strip() in hotel_name:
                #             default_data['hotel_name'] = key
                #             default_data['hotel_star'] = value['hotel_star']
            except:
                continue
        return list(result.values())
    #
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

    def get_kih_data(self):
        result = []
        # ---
        with ThreadPoolExecutor(max_workers=85) as executor:
            # # #

            #=== Eghamat24========
            eghamat = Eghamat24(self.target, self.start_date, self.end_date, self.adults)
            eghamat = executor.submit(eghamat.get_result)
            #====================


            # --- moghim24
            moghim = Moghim24(self.target, self.start_date, self.end_date, self.adults)
            moghim = executor.submit(moghim.get_result)
            #
            # # # --- deltaban
            deltaban = Deltaban(self.target, self.start_date, self.end_date, self.adults)
            deltaban = executor.submit(deltaban.get_result)
            # # --- alwin
            alwin = Alwin24(self.target, self.start_date, self.end_date, self.adults)
            alwin = executor.submit(alwin.get_result)
            # # --- booking
            booking = Booking(self.target, self.start_date, self.end_date, self.adults)
            booking = executor.submit(booking.get_result)
            # # --- rahbal
            rahbal = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal')
            rahbal = executor.submit(rahbal.get_result)
            # --- HRC
            hrc = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HRC, 'hrc')
            hrc = executor.submit(hrc.get_result)
            # --- DAYAN
            dayan = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DAYAN, 'dayan')
            dayan = executor.submit(dayan.get_result)
            # --- OMID_OJ
            omid_oj = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, OMID_OJ, 'omid_oj')
            omid_oj = executor.submit(omid_oj.get_result)
            # --- SEPID_PARVAZ
            sepid_parvaz = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SEPID_PARVAZ,
                                       'sepid_parvaz')
            sepid_parvaz = executor.submit(sepid_parvaz.get_result)
            # --- PARMIS
            parmis = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, PARMIS, 'parmis')
            parmis = executor.submit(parmis.get_result)
            # --- MEHRAB
            mehrab = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab')
            mehrab = executor.submit(mehrab.get_result)
            # --- HAMSAFAR
            hamsafar = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMSAFAR, 'hamsafar')
            hamsafar = executor.submit(hamsafar.get_result)
            # --- TAK_SETAREH
            tak_setareh = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,
                                      'tak_setareh')
            tak_setareh = executor.submit(tak_setareh.get_result)

            # --- Kimiya
            kimiya = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TOURISTKISH,
                                      'kimiya')
            kimiya = executor.submit(kimiya.get_result)

            # --- Eram
            eram2mhd = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, ERAM2MHD,
                                      'eram2mhd')
            eram2mhd = executor.submit(eram2mhd.get_result)

            # --- SHAYAN GASHT
            shayan_gasht = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,
                                       'shayan_gasht')
            shayan_gasht = executor.submit(shayan_gasht.get_result)


            #--- eghamat24
            try:
                eghamat=eghamat.result(timeout=10000)
            except:
                eghamat=[]


            #--- moghim24
            try:
                kimiya=kimiya.result(timeout=1000)
            except:
                kimiya=[]

            try:
                eram2mhd=eram2mhd.result(timeout=1000)
            except:
                eram2mhd=[]
            try:
                shayan_gasht=shayan_gasht.result(timeout=1000)
            except:
                shayan_gasht=[]

            #--- moghim24
            try:
                moghim=moghim.result(timeout=1000)
            except:
                moghim=[]

            #
            # --- deltaban
            try:
                deltaban = deltaban.result(timeout=4000)
            except:
                deltaban = []
            # # # --- alwin
            try:
                alwin = alwin.result(timeout=400000)
            except:
                alwin = []
            # # --- booking
            try:
                booking = booking.result(timeout=400000)
            except:
                booking = []
            # --- rahbal
            try:
                rahbal = rahbal.result(timeout=4000)
            except:
                rahbal = []
            # --- hrc
            try:
                hrc = hrc.result(timeout=40)
            except:
                hrc = []
            # --- dayan
            try:
                dayan = dayan.result(timeout=4000)
            except:
                dayan = []
            # --- omid_oj
            try:
                omid_oj = omid_oj.result(timeout=4000)
            except:
                omid_oj = []
            # --- sepid_parvaz
            try:
                sepid_parvaz = sepid_parvaz.result(timeout=4000)
            except:
                sepid_parvaz = []
            # --- mehrab
            try:
                mehrab = mehrab.result(timeout=50000)
            except:
                mehrab = []
            # --- parmis
            try:
                parmis = parmis.result(timeout=4000)
            except:
                parmis = []
            # --- hamsafar
            try:
                hamsafar = hamsafar.result(timeout=4000)
            except:
                hamsafar = []
            # --- tak_setareh
            try:
                tak_setareh = tak_setareh.result(timeout=4000)
            except:
                tak_setareh = []
            # ---
            print("--------------------------------")
            print("eghamat => ", len(eghamat))
            print("moghim => ", len(moghim))
            print("shayan_gasht => ", len(shayan_gasht))
            print("kimiya => ", len(kimiya))
            print("eram2mhd => ", len(eram2mhd))
            print("alwin => ", len(alwin))
            print("deltaban => ", len(deltaban))
            print("booking => ", len(booking))
            print("rahbal => ", len(rahbal))
            print("hrc => ", len(hrc))
            print("dayan => ", len(dayan))
            print("omid oj => ", len(omid_oj))
            print("sepid parvaz => ", len(sepid_parvaz))
            print("mehrab => ", len(mehrab))
            print("parmis => ", len(parmis))
            print("hamsafar => ", len(hamsafar))
            print("tak_setareh => ", len(tak_setareh))
            # # # ---
            # #
            # #
            # # #============
            # # # Integration (ramin)
            # # #=========
            # #
            #
            # #====================
            result.extend(eghamat)
            result.extend(moghim)
            result.extend(eram2mhd)
            result.extend(kimiya)
            result.extend(shayan_gasht)
            result.extend(alwin)
            result.extend(deltaban)
            result.extend(booking)
            result.extend(rahbal)
            result.extend(hrc)
            result.extend(dayan)
            result.extend(omid_oj)
            result.extend(sepid_parvaz)
            result.extend(mehrab)
            result.extend(parmis)
            result.extend(hamsafar)
            result.extend(tak_setareh)
        # ---
        return self.ready_data(result, "KIH")

    def get_gsm_data(self):
        result = []
        # ---
        with ThreadPoolExecutor(max_workers=85) as executor:



            #=== Eghamat24========
            eghamat = Eghamat24(self.target, self.start_date, self.end_date, self.adults)
            eghamat = executor.submit(eghamat.get_result)
            #====================

            # # --- booking
            booking = Booking(self.target, self.start_date, self.end_date, self.adults)
            booking = executor.submit(booking.get_result)

            # --- TAK_SETAREH
            tak_setareh = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,
                                      'tak_setareh')
            tak_setareh = executor.submit(tak_setareh.get_result)

            # # --- rahbal
            rahbal = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal')
            rahbal = executor.submit(rahbal.get_result)

            # --- MEHRAB
            mehrab = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab')
            mehrab = executor.submit(mehrab.get_result)



            # --- alwin
            alwin = Alwin24(self.target, self.start_date, self.end_date, self.adults)
            alwin = executor.submit(alwin.get_result)
            # --- IMAN
            iman = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, IMAN, 'iman')
            iman = executor.submit(iman.get_result)
            # --- FLAMINGO
            flamingo = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, FLAMINGO, 'flamingo')
            flamingo = executor.submit(flamingo.get_result)
            # --- SHAYAN GASHT
            shayan_gasht = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,
                                       'shayan_gasht')
            shayan_gasht = executor.submit(shayan_gasht.get_result)
            # # --- DOLFIN
            dolfin = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DOLFIN, 'dolfin')
            dolfin = executor.submit(dolfin.get_result)
            # # --- YEGANE FARD
            yegane_fard = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, YEGANE_FARD,
                                      'yegane_fard')
            yegane_fard = executor.submit(yegane_fard.get_result)

            # # --- safiran
            safiran = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SAFIRAN,
                                      'safiran')
            safiran = executor.submit(safiran.get_result)

            # # --- hamood
            hamood = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMOOD,
                                      'hamood')
            hamood = executor.submit(hamood.get_result)



            # --- eghamat
            try:
                eghamat = eghamat.result(timeout=40)
            except:
                eghamat = []


            # --- tak_setareh
            try:
                tak_setareh = tak_setareh.result(timeout=40)
            except:
                tak_setareh = []

            # --- rahbal
            try:
                rahbal = rahbal.result(timeout=40)
            except:
                rahbal = []

            # --- mehrab
            try:
                mehrab = mehrab.result(timeout=40)
            except:
                mehrab = []




            # --- ALWIN
            try:
                alwin = alwin.result(timeout=40)
            except:
                alwin = []
            # --- booking
            try:
                booking = booking.result(timeout=400)
            except:
                booking = []

            # --- IMAN
            try:
                iman = iman.result(timeout=40)
            except:
                iman = []
            # --- FLAMINGO
            try:
                flamingo = flamingo.result(timeout=40)
            except:
                flamingo = []
            # --- SHAYAN GASHT
            try:
                shayan_gasht = shayan_gasht.result(timeout=40)
            except:
                shayan_gasht = []
            # --- DOLFIN
            try:
                dolfin = dolfin.result(timeout=40)
            except:
                dolfin = []
            # --- YEGANE FARD
            try:
                yegane_fard = yegane_fard.result(timeout=40)
            except:
                yegane_fard = []


            # --- tak_setareh
            try:
                safiran = safiran.result(timeout=40)
            except:
                safiran = []

            # --- hamood
            try:
                hamood = hamood.result(timeout=40)
            except:
                hamood = []





            # ---
            print("--------------------------------")
            print("eghamat => ", len(eghamat))
            print("alwin => ", len(alwin))
            print("tak_setareh => ", len(tak_setareh))
            print("mehrab => ", len(mehrab))
            print("rahbal => ", len(rahbal))
            print("booking => ", len(booking))
            print("iman => ", len(iman))
            print("flamingo => ", len(flamingo))
            print("shayan_gasht => ", len(shayan_gasht))
            print("dolfin => ", len(dolfin))
            print("yegane_fard => ", len(yegane_fard))
            print("safiran => ", len(safiran))
            print("hamood => ", len(hamood))
            # ---
            result.extend(eghamat)
            result.extend(alwin)
            result.extend(tak_setareh)
            result.extend(rahbal)
            result.extend(mehrab)
            result.extend(booking)
            result.extend(iman)
            result.extend(flamingo)
            result.extend(shayan_gasht)
            result.extend(dolfin)
            result.extend(yegane_fard)
            result.extend(safiran)
            result.extend(hamood)
        # ---
        # return self.ready_data(result, "GSM")
        return self.read_data_GSM(result)


    #=== koli hazer konid!!!

    def get_ALLDestination_data(self):
        result = []
        # ---
        with ThreadPoolExecutor(max_workers=85) as executor:
            # # #

            #=== Alaedin ===
            alaedin=Alaedin(self.target,self.start_date,self.end_date,self.adults)
            alaedin = executor.submit(alaedin.get_result)
            #===========

            #=== FlyToday ===
            flytoday=FlyToday(self.target,self.start_date,self.end_date,self.adults)
            flytoday = executor.submit(flytoday.get_result)
            #===========

            #=== Eghamat24========
            eghamat = Eghamat24(self.target, self.start_date, self.end_date, self.adults)
            eghamat = executor.submit(eghamat.get_result)
            # # ====================


            # # --- moghim24
            # moghim = Moghim24(self.target, self.start_date, self.end_date, self.adults)
            # moghim = executor.submit(moghim.get_result)
            #



            # # # --- deltaban
            deltaban = Deltaban(self.target, self.start_date, self.end_date, self.adults)
            deltaban = executor.submit(deltaban.get_result)

            # # --- alwin
            alwin = Alwin24(self.target, self.start_date, self.end_date, self.adults)
            alwin = executor.submit(alwin.get_result)



            # # --- booking
            booking = Booking(self.target, self.start_date, self.end_date, self.adults)
            booking = executor.submit(booking.get_result)
            # # --- rahbal
            rahbal = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, RAHBAL, 'rahbal')
            rahbal = executor.submit(rahbal.get_result)
            # --- HRC
            hrc = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HRC, 'hrc')
            hrc = executor.submit(hrc.get_result)
            # --- DAYAN
            dayan = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DAYAN, 'dayan')
            dayan = executor.submit(dayan.get_result)
            # --- OMID_OJ
            omid_oj = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, OMID_OJ, 'omid_oj')
            omid_oj = executor.submit(omid_oj.get_result)
            # --- SEPID_PARVAZ
            sepid_parvaz = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SEPID_PARVAZ,
                                       'sepid_parvaz')
            sepid_parvaz = executor.submit(sepid_parvaz.get_result)
            # --- PARMIS
            parmis = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, PARMIS, 'parmis')
            parmis = executor.submit(parmis.get_result)
            # --- MEHRAB
            mehrab = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, MEHRAB, 'mehrab')
            mehrab = executor.submit(mehrab.get_result)
            # --- HAMSAFAR
            hamsafar = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, HAMSAFAR, 'hamsafar')
            hamsafar = executor.submit(hamsafar.get_result)
            # --- TAK_SETAREH
            tak_setareh = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TAK_SETAREH,
                                      'tak_setareh')
            tak_setareh = executor.submit(tak_setareh.get_result)

            # --- Kimiya
            kimiya = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, TOURISTKISH,
                                      'kimiya')
            kimiya = executor.submit(kimiya.get_result)

            # --- Eram
            eram2mhd = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, ERAM2MHD,
                                      'eram2mhd')
            eram2mhd = executor.submit(eram2mhd.get_result)

            # --- SHAYAN GASHT
            shayan_gasht = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, SHAYAN_GASHT,
                                       'shayan_gasht')
            shayan_gasht = executor.submit(shayan_gasht.get_result)




            # --- ALAEDIN
            try:
                alaedin = alaedin.result(timeout=10000)
            except:
                alaedin = []

            #--- FlyToday
            try:
                flytoday=flytoday.result(timeout=10000)
            except:
                flytoday=[]




            #--- eghamat24
            try:
                eghamat=eghamat.result(timeout=1000)
            except:
                eghamat=[]
            # eghamat = []


            #--- moghim24
            try:
                kimiya=kimiya.result(timeout=1000)
            except:
                kimiya=[]

            try:
                eram2mhd=eram2mhd.result(timeout=1000)
            except:
                eram2mhd=[]
            try:
                shayan_gasht=shayan_gasht.result(timeout=1000)
            except:
                shayan_gasht=[]

            # #--- moghim24
            # try:
            #     moghim=moghim.result(timeout=1000)
            # except:
            #     moghim=[]

            #
            # --- deltaban
            try:
                deltaban = deltaban.result(timeout=400000)
            except:
                deltaban = []
            # deltaban = []
            # # # --- alwin
            try:
                alwin = alwin.result(timeout=400000)
            except:
                alwin = []
            # alwin = []

            # # --- booking
            try:
                booking = booking.result(timeout=400000)
            except:
                booking = []
            # --- rahbal
            try:
                rahbal = rahbal.result(timeout=4000)
            except:
                rahbal = []
            # --- hrc
            try:
                hrc = hrc.result(timeout=40)
            except:
                hrc = []
            # --- dayan
            try:
                dayan = dayan.result(timeout=4000)
            except:
                dayan = []
            # --- omid_oj
            try:
                omid_oj = omid_oj.result(timeout=4000)
            except:
                omid_oj = []
            # --- sepid_parvaz
            try:
                sepid_parvaz = sepid_parvaz.result(timeout=4000)
            except:
                sepid_parvaz = []
            # --- mehrab
            try:
                mehrab = mehrab.result(timeout=50000)
            except:
                mehrab = []
            # --- parmis
            try:
                parmis = parmis.result(timeout=4000)
            except:
                parmis = []
            # --- hamsafar
            try:
                hamsafar = hamsafar.result(timeout=4000)
            except:
                hamsafar = []
            # --- tak_setareh
            try:
                tak_setareh = tak_setareh.result(timeout=4000)
            except:
                tak_setareh = []
            # ---
            print("--------------------------------")
            print("alaedin => ", len(alaedin))
            print("flytoday => ", len(flytoday))
            print("eghamat => ", len(eghamat))
            # print("moghim => ", len(moghim))
            print("shayan_gasht => ", len(shayan_gasht))
            print("kimiya => ", len(kimiya))
            print("eram2mhd => ", len(eram2mhd))
            print("alwin => ", len(alwin))
            print("deltaban => ", len(deltaban))
            print("booking => ", len(booking))
            print("rahbal => ", len(rahbal))
            print("hrc => ", len(hrc))
            print("dayan => ", len(dayan))
            print("omid oj => ", len(omid_oj))
            print("sepid parvaz => ", len(sepid_parvaz))
            print("mehrab => ", len(mehrab))
            print("parmis => ", len(parmis))
            print("hamsafar => ", len(hamsafar))
            print("tak_setareh => ", len(tak_setareh))
            # # # ---
            # #
            # #
            # # #============
            # # # Integration (ramin)
            # # #=========
            # #
            #
            # #====================
            result.extend(alaedin)
            result.extend(flytoday)
            result.extend(eghamat)
            # result.extend(moghim)
            result.extend(eram2mhd)
            result.extend(kimiya)
            result.extend(shayan_gasht)
            result.extend(alwin)
            result.extend(deltaban)
            result.extend(booking)
            result.extend(rahbal)
            result.extend(hrc)
            result.extend(dayan)
            result.extend(omid_oj)
            result.extend(sepid_parvaz)
            result.extend(mehrab)
            result.extend(parmis)
            result.extend(hamsafar)
            result.extend(tak_setareh)
        # ---
        return self.read_data_ALLDestination(result)


    #====




    def get_result(self):

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
        if check_redis_key(redis_key):
            return get_dict_to_redis(redis_key)
        else:
            if self.target == "KIH":
                result = self.get_kih_data()
            elif self.target == "GSM":
                result = self.get_gsm_data()
            else:
                result=self.get_ALLDestination_data()

            if len(result):
                add_dict_to_redis(redis_key, result, self.redis_expire)


            # #----- saved --
            # import json
            # aa=json.dumps(result)
            # fp=open('result.json','w',encoding='utf8')
            # fp.write(aa)
            # fp.close()


            return result
