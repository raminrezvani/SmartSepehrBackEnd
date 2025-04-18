import os
os.system("title Crawl Eghamat24_service_OK")
from flask import Flask, jsonify, request
import json
from lxml import etree
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
import requests
# from insert_influx import Influxdb
# influx = Influxdb()
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=100)
# executor = ThreadPoolExecutor(max_workers=1)
class Eghamat24:
    def __init__(self, target='MHD', startdate='2024-10-16', stay='3',isAnalysiss=False,hotelstarAnalysis=[],priorityTimestamp=1,
                 use_cache=0):
        self.target = target
        self.startdate = startdate
        self.stay = stay
        # self.isAnalysis=isAnalysis
        self.isAnalysis=isAnalysiss[0] if isAnalysiss is tuple else isAnalysiss ,
        self.isAnalysis = self.isAnalysis[0] if isinstance(self.isAnalysis, tuple) else self.isAnalysis

        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp=priorityTimestamp
        self.use_cache=use_cache
        # self.executor = ThreadPoolExecutor(max_workers=100)
        self.hotelResults = list()

    def convert_to_number(self, persian_number):
        persian_to_arabic = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        converted_number = persian_number.translate(persian_to_arabic).replace(',', '')
        try:
            return int(converted_number)
        except:
            return 'نامشخص'

    def get_one_hotel_Data(self, hotel):
        property_id = hotel['property_id']
        url = f'https://www.eghamat24.com/property-rooms/list-view?property_id={property_id}&check_in={self.startdate}&length_of_stay={self.stay}'
        res = requests.get(url).text
        # influx.capture_logs(1, 'Eghamat24')
        parser = etree.HTMLParser()
        htmlparsed = etree.parse(StringIO(res), parser=parser)


        lst_hotelRow=htmlparsed.xpath('//div[contains(@class,"p-room card")]')


        lst_items = [a.xpath('.//div[@class="mb-3 mb-md-4"]')[0] for a in lst_hotelRow]
        lst_items_text = [' '.join(a.xpath('span/text()')).split('\r')[0] for a in lst_items]
        lst_prices =[a.xpath('.//div[@class="subtitle-3 fw-semibold fw-md-bold"]/text()')[0] for a in lst_hotelRow]
        lst_prices_text = [a.replace('\r\n', '').replace('تومان', '').strip() for a in lst_prices]

        lst_capacities = [a.xpath('.//div[@class="d-flex flex-wrap body-2 mb-3 mb-md-2"]/span/text()')[0] for a in lst_hotelRow]
        lst_capacities_text = [a.replace('\r\n', '').split('نفر')[0].replace('نفره', '').replace('-', '').replace('  ', '').strip() for a in lst_capacities]
        # lst_buttons = [a.xpath('.//button[@type="submit"]')[0] for a in lst_hotelRow]


        one_hotelResults = {
            'hotel_name': hotel['title'],
            'hotel_star': hotel['star'],
            'provider': 'Eghamat24',
            'min_price': '',
            'rooms': []
        }

        for iter in range(len(lst_items_text)):

            # چک کردن قابل رزرو بودن
            try:
                available=lst_hotelRow[iter].xpath('.//button[@type="submit"]')[0].text
            except:
                # قابل رزرو نیست
                continue


            dic = {
                'name': lst_items_text[iter],
                'price': self.convert_to_number(lst_prices_text[iter]),
                'capacity':lst_capacities_text[iter],
                'provider': 'Eghamat24'
            }
            one_hotelResults['rooms'].append(dic)


        try:
            one_hotelResults['min_price'] = min(
                int(room['price']) for room in one_hotelResults['rooms'] if room['price'] != 'نامشخص'
            )
        except:
            print('error_')
            one_hotelResults['min_price'] = 'نامشخص'

        # print('Eghamat24     '+hotel['title'])
        self.hotelResults.append(one_hotelResults)










    def get_data(self):
        # with open(f'eghamat_data/lstHotels_{self.target}_withProperty.json', 'r', encoding='utf-8') as file:
        with open(f'eghamat_data/lstHotels_{self.target}_withProperty.json', 'r', encoding='utf-8') as file:
            lst_items_ok = json.load(file)




        #======== Check for hotel names or star ratings
        if self.isAnalysis!='0':
            # Create a set of all hotel names for faster lookup
            all_hotel_names = {hotel['title'] for hotel in lst_items_ok}
            selected_hotels = set()  # Using set to avoid duplicates

            # Check Redis for hotel name mappings
            for hotel_star in self.hotelstarAnalysis:
                redis_key = f"asli_hotel:{hotel_star}"
                redis_data = redis_client.get(redis_key)
                if redis_data:
                    mapped_hotels = json.loads(redis_data)
                    # Add hotels that exist in our current hotels list
                    selected_hotels.update(hotel for hotel in mapped_hotels if hotel in all_hotel_names)

            if selected_hotels:
                # If we found mapped hotels, filter the hotels list
                lst_items_ok = [hotel for hotel in lst_items_ok if hotel['title'] in selected_hotels]
            else:
                # Fallback to original star rating and name check
                lst_items_ok = [hotel for hotel in lst_items_ok
                         if (str(hotel['star']) in self.hotelstarAnalysis)
                         or (hotel['title'] in self.hotelstarAnalysis)]

            print(f'Eghamat Analysis')
        else:
            print(f'Eghamat RASII')

        #============


        # # #---------- Check 5-Star of hotel
        # if (self.isAnalysis == '1'):
        #     lst_items_ok = [htl for htl in lst_items_ok if str(htl['star']) in self.hotelstarAnalysis]
        #     print('Eghamat Analysis')
        # else:
        #     print('Eghamat RASII')
        # # #------------------------


        lst_thread = []
        for hotel in lst_items_ok:
            lst_thread.append(executor.submit(self.get_one_hotel_Data, hotel))

        for th in lst_thread:
            th.result()

    def get_hotelResults(self):
        return self.hotelResults

@app.route('/fetch_hotels', methods=['GET'])
def fetch_hotels():
    target = request.args.get('target', 'MHD')
    startdate = request.args.get('startdate', '2024-10-16')
    stay = request.args.get('stay', '3')
    isAnalysis = request.args.get('isAnalysis')

    hotelstarAnalysis=request.args.get('hotelstarAnalysis')
    hotelstarAnalysis=json.loads(hotelstarAnalysis)
    priorityTimestamp = request.args.get('priorityTimestamp')
    use_cache = request.args.get('use_cache')

    eghamat = Eghamat24(target, startdate, stay,isAnalysis,hotelstarAnalysis,priorityTimestamp,use_cache)
    eghamat.get_data()
    results = eghamat.get_hotelResults()
    return jsonify(results)

if __name__ == '__main__':
    # app.run(debug=True,port=8022,host='0.0.0.0')
    app.run(debug=False,port=8022,host='0.0.0.0')

