from concurrent.futures import ThreadPoolExecutor

from app_crawl.flight.sepehr360 import Sepehr360
from app_crawl.flight.Flight_flytoday import FlyToDay


from app_crawl.flight.mojalalsafar_crawler import MojalalSafar
# from app_crawl.flight.alibaba import Alibaba
from app_crawl.helpers import convert_gregorian_date_to_persian


import jdatetime
from datetime import datetime
def get_Duration(departure_date_str,departure_time_str,return_date_str,return_time_str,
                 another_date_str,another_time_str):
    def jalali_to_gregorian(jalali_date):
        jalali_year, jalali_month, jalali_day = map(int, jalali_date.split('/'))
        gregorian_date = jdatetime.date(jalali_year, jalali_month, jalali_day).togregorian()
        return gregorian_date

    # departure_date_str = "1403/06/05"
    # departure_time_str = "23:30"
    #
    # return_date_str = "1403/06/06"
    # return_time_str = "00:45"

    departure_date = jalali_to_gregorian(departure_date_str)
    return_date = jalali_to_gregorian(return_date_str)

    departure_datetime = datetime.combine(departure_date, datetime.strptime(departure_time_str, "%H:%M").time())
    return_datetime = datetime.combine(return_date, datetime.strptime(return_time_str, "%H:%M").time())

    duration = return_datetime - departure_datetime

    # # تاریخ و زمان دیگر
    # another_date_str = "1403/06/06"
    # another_time_str = "23:00"

    # ترکیب تاریخ و زمان دیگر
    another_date = jalali_to_gregorian(another_date_str)
    another_datetime = datetime.combine(another_date, datetime.strptime(another_time_str, "%H:%M").time())

    # اضافه کردن مدت زمان محاسبه شده به تاریخ و زمان جدید
    new_datetime = another_datetime + duration

    # تبدیل تاریخ میلادی جدید به شمسی
    new_jalali_date = jdatetime.datetime.fromgregorian(datetime=new_datetime)

    # جدا کردن تاریخ و زمان
    new_jalali_date_str = new_jalali_date.strftime("%Y/%m/%d")
    new_jalali_time_str = new_jalali_date.strftime("%H:%M")
    #
    # print(f"تاریخ جدید: {new_jalali_date_str}")
    # print(f"زمان جدید: {new_jalali_time_str}")


    return new_jalali_date_str,new_jalali_time_str

class Flight:
    def __init__(self, start_date, end_date, source, target, one_way):
        self.start_date = start_date
        self.end_date = end_date
        self.persian_start_date = convert_gregorian_date_to_persian(start_date, "%Y/%m/%d")['date']
        self.persian_end_date = convert_gregorian_date_to_persian(end_date, "%Y/%m/%d")['date']
        self.source = source
        self.target = target
        self.one_way = one_way
        self.executor = ThreadPoolExecutor(max_workers=50)

    def ready_data(self, data):
        if self.one_way:
            result = {}
            # ---
            for flight in data:
                # if ('مجلل سفر طلایی' in flight['provider_name']):
                #     print('df')
                flight_key = f"{flight['airline_code']}-{flight['flight_number']}"
                default_data = {
                    "airline_name": flight['airline_name'],
                    "airline_code": flight['airline_code'],
                    "go_time": flight['go_time'],
                    "go_date": flight['go_date'],
                    "return_time": flight['return_time'],
                    'return_date': flight['return_date'],
                    "flight_number": flight['flight_number'],
                    'min_price': flight['price'],
                    "providers": []
                }
                result.setdefault(flight_key, default_data)
                result[flight_key]['providers'].append(flight)
                # ---
                if result[flight_key]['min_price'] >= flight['price']:
                    result[flight_key]['min_price'] = flight['price']
                # ---
                result[flight_key]['providers'] = sorted(result[flight_key]['providers'], key=lambda fl: fl['price'])
            # ---
            return list(result.values())
        else:
            result = {
                "go_flight": {},
                "return_flight": {}
            }
            # ---
            for flight in data['go_flight']:
                flight_key = f"{flight['airline_code']}-{flight['flight_number']}"
                default_data = {
                    "airline_name": flight['airline_name'],
                    "airline_code": flight['airline_code'],
                    "go_time": flight['go_time'],
                    "go_date": flight['go_date'],
                    "return_time": flight['return_time'],
                    'return_date': flight['return_date'],
                    "flight_number": flight['flight_number'],
                    'min_price': flight['price'],
                    "providers": []
                }
                result['go_flight'].setdefault(flight_key, default_data)
                result['go_flight'][flight_key]['providers'].append(flight)
                # ---
                if result['go_flight'][flight_key]['min_price'] >= flight['price']:
                    result['go_flight'][flight_key]['min_price'] = flight['price']
                # ---
                result['go_flight'][flight_key]['providers'] = sorted(result['go_flight'][flight_key]['providers'],
                                                                      key=lambda fl: fl['price'])

            #=== sort all ===
            # Sort the flights by the price of the first provider  (OKOKOKOKK)
            result['go_flight'] = dict(sorted(result['go_flight'].items(), key=lambda x: x[1]['providers'][0]['price']))
            # #====


            # ---
            for flight in data['return_flight']:
                flight_key = f"{flight['airline_code']}-{flight['flight_number']}"
                default_data = {
                    "airline_name": flight['airline_name'],
                    "airline_code": flight['airline_code'],
                    "go_time": flight['go_time'],
                    "go_date": flight['go_date'],
                    "return_time": flight['return_time'],
                    'return_date': flight['return_date'],
                    "flight_number": flight['flight_number'],
                    'min_price': flight['price'],
                    "providers": []
                }
                result['return_flight'].setdefault(flight_key, default_data)
                result['return_flight'][flight_key]['providers'].append(flight)
                # ---
                if result['return_flight'][flight_key]['min_price'] >= flight['price']:
                    result['return_flight'][flight_key]['min_price'] = flight['price']
                # ---
                result['return_flight'][flight_key]['providers'] = sorted(
                    result['return_flight'][flight_key]['providers'],
                    key=lambda fl: fl['price'])

            #=== sort all ===
            # Sort the flights by the price of the first provider  (OKOKOKOKK)
            result['return_flight'] = dict(sorted(result['return_flight'].items(), key=lambda x: x[1]['providers'][0]['price']))
            # #====


            # ---
            result['go_flight'] = list(result['go_flight'].values())
            result['return_flight'] = list(result['return_flight'].values())
            return result

    def get_result(self):
        # --- sepehr
        sepehr360 = Sepehr360(self.start_date, self.end_date, self.source, self.target)
        sepehr360 = self.executor.submit(sepehr360.get_result, self.one_way)

        # --- sepehr
        mojalalsafar = MojalalSafar(self.start_date, self.end_date, self.source, self.target)
        mojalalsafar = self.executor.submit(mojalalsafar.get_result, self.one_way)


        # #=== flytoday
        # flytoday=FlyToDay(self.start_date,self.source,self.target)
        # flytoday = self.executor.submit(flytoday.get_result)

        # --- alibaba
        # alibaba = Alibaba(self.start_date, self.end_date, self.source, self.target)
        # alibaba = self.executor.submit(alibaba.get_result, self.one_way)
        # ---
        if self.one_way:
            result = []
            # ---
            sepehr360 = sepehr360.result()
            mojalalsafar=mojalalsafar.result()
            # flytoday=flytoday.result()
            # alibaba = alibaba.result()



            #========== Get return_time and return_date for Mojalalsafar
            for item in range(len(mojalalsafar)):
                try:
                    mojalalsafar[item]['return_date'],mojalalsafar[item]['return_time']=get_Duration(sepehr360[0]['go_date'], sepehr360[0]['go_time'],
                                                                                       sepehr360[0]['return_date'],  sepehr360[0]['return_time'],
                                 mojalalsafar[item]['go_date'], mojalalsafar[item]['go_time'])
                except:
                    continue

            #===================================
            # ---
            result.extend(sepehr360)
            result.extend(mojalalsafar)
            # result.extend(flytoday)
            # result.extend(alibaba)




        else:  #two-way
            result = {"go_flight": [], "return_flight": []}
            # ---
            sepehr360 = sepehr360.result()
            mojalalsafar = mojalalsafar.result()
            # alibaba = alibaba.result()
            # ---
            result['go_flight'].extend(sepehr360['go_flight'])
            result['go_flight'].extend(mojalalsafar['go_flight'])
            # result['go_flight'].extend(alibaba['go_flight'])
            # ---
            result['return_flight'].extend(sepehr360['return_flight'])
            result['return_flight'].extend(mojalalsafar['return_flight'])
            # result['return_flight'].extend(alibaba['return_flight'])
        # --- return
        return self.ready_data(result)

# from time import perf_counter
#
#
# start = perf_counter()
# flight = Flight("2023-01-30", "2023-02-02", "MHD", "THR", False)
# print("--------------------------------")
# print(flight.get_result())
# end = perf_counter()
#
# print("--------------------------------")
# print(f"end with ==> {round(end - start, 2)} seconds")
