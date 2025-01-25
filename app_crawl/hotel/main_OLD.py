from .deltaban import Deltaban
from .booking import Booking
from .alwin import Alwin24
from app_crawl.helpers import (add_dict_to_redis, get_dict_to_redis, check_redis_key, ready_sepehr_gsm_hotel_name,
                               ready_sepehr_hotel_name)
from app_crawl.gsm.data import hotels
from concurrent.futures import ThreadPoolExecutor
from app_crawl.hotel.sepehr import SepehrHotel
from app_crawl.cookie.cookie_data import (RAHBAL, HRC, DAYAN, OMID_OJ, SEPID_PARVAZ, PARMIS, HAMSAFAR, MEHRAB,
                                          TAK_SETAREH, IMAN, FLAMINGO, SHAYAN_GASHT, DOLFIN, YEGANE_FARD)
from app_crawl.kih.data import hotels


class Hotel:
    def __init__(self, source, target, start_date, end_date, adults):
        self.source = source
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.redis_expire = 0  # 3 minutes

    def ready_data(self, data, target):
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
                for key, value in hotels.items():
                    system_provider = value[hotel['provider']]
                    if system_provider:
                        if system_provider.strip() in hotel_name:
                            default_data['hotel_name'] = key
                            default_data['hotel_star'] = value['hotel_star']
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

    def get_kih_data(self):
        result = []
        # ---
        with ThreadPoolExecutor(max_workers=85) as executor:
            # --- deltaban
            deltaban = Deltaban(self.target, self.start_date, self.end_date, self.adults)
            deltaban = executor.submit(deltaban.get_result)
            # --- alwin
            alwin = Alwin24(self.target, self.start_date, self.end_date, self.adults)
            alwin = executor.submit(alwin.get_result)
            # --- booking
            booking = Booking(self.target, self.start_date, self.end_date, self.adults)
            booking = executor.submit(booking.get_result)
            # --- rahbal
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
            # --- deltaban
            try:
                deltaban = deltaban.result(timeout=40)
            except:
                deltaban = []
            # --- alwin
            try:
                alwin = alwin.result(timeout=40)
            except:
                alwin = []
            # --- booking
            try:
                booking = booking.result(timeout=40)
            except:
                booking = []
            # --- rahbal
            try:
                rahbal = rahbal.result(timeout=40)
            except:
                rahbal = []
            # --- hrc
            try:
                hrc = hrc.result(timeout=40)
            except:
                hrc = []
            # --- dayan
            try:
                dayan = dayan.result(timeout=40)
            except:
                dayan = []
            # --- omid_oj
            try:
                omid_oj = omid_oj.result(timeout=40)
            except:
                omid_oj = []
            # --- sepid_parvaz
            try:
                sepid_parvaz = sepid_parvaz.result(timeout=40)
            except:
                sepid_parvaz = []
            # --- mehrab
            try:
                mehrab = mehrab.result(timeout=500)
            except:
                mehrab = []
            # --- parmis
            try:
                parmis = parmis.result(timeout=40)
            except:
                parmis = []
            # --- hamsafar
            try:
                hamsafar = hamsafar.result(timeout=40)
            except:
                hamsafar = []
            # --- tak_setareh
            try:
                tak_setareh = tak_setareh.result(timeout=40)
            except:
                tak_setareh = []
            # ---
            print("--------------------------------")
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
            # ---
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
            # --- DOLFIN
            dolfin = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, DOLFIN, 'dolfin')
            dolfin = executor.submit(dolfin.get_result)
            # --- YEGANE FARD
            yegane_fard = SepehrHotel(self.target, self.start_date, self.end_date, self.adults, YEGANE_FARD,
                                      'yegane_fard')
            yegane_fard = executor.submit(yegane_fard.get_result)
            # --- ALWIN
            try:
                alwin = alwin.result(timeout=40)
            except:
                alwin = []
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
            # ---
            print("--------------------------------")
            print("alwin => ", len(alwin))
            print("iman => ", len(iman))
            print("flamingo => ", len(flamingo))
            print("shayan_gasht => ", len(shayan_gasht))
            print("dolfin => ", len(dolfin))
            print("yegane_fard => ", len(yegane_fard))
            # ---
            result.extend(alwin)
            result.extend(iman)
            result.extend(flamingo)
            result.extend(shayan_gasht)
            result.extend(dolfin)
            result.extend(yegane_fard)
        # ---
        return self.ready_data(result, "GSM")

    def get_result(self):
        redis_key = f"{self.source}_{self.target}_{self.start_date}_{self.end_date}_{self.adults}"
        if check_redis_key(redis_key):
            return get_dict_to_redis(redis_key)
        else:
            if self.target == "KIH":
                result = self.get_kih_data()
            elif self.target == "GSM":
                result = self.get_gsm_data()
            else:
                result = []
            if len(result):
                add_dict_to_redis(redis_key, result, self.redis_expire)
            return result
