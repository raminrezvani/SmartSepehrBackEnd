from concurrent.futures import ThreadPoolExecutor, wait,as_completed


import urllib3

from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import jdatetime
import os
from lxml import etree
from io import StringIO
import requests
from app_crawl.hotel.Client_Dispatch_requests import executeRequest
import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_CONFIG['HOST'],
    port=settings.REDIS_CONFIG['PORT'],
    db=settings.REDIS_CONFIG['DB'],
    decode_responses=settings.REDIS_CONFIG['DECODE_RESPONSES']
)

destin_text={
            'KIH':'kish',
            'THR':'tehran',
            'IFN':'isfahan',
            'MHD':'mashhad',
            'TBZ':'tabriz',
            'SYZ':'shiraz',
            'GSM':'qeshm',
            'AZD':'yazd',
            'AWZ':'ahvaz',
            'BND':'bandarabbas',
            'KER':'kerman',
            'KSH':'kermanshah',
            'RAS':'rasht',
            'SRY':'sari',
            'ZBR':'chabahar',

            # =========
            'ABD': 'abadan',
            'BUZ': 'bushehr',
            'GBT': 'gorgan',
            'OMH': 'urmia',
            'ADU': 'ardabil',
            'HDM': 'hamadan',
            'RZR': 'ramsar',
            'KHD': 'khorramabad',
            'NSH': 'nowshahr',
            # ===========



        }

class Alaedin:
    def __init__(self, target, start_date, end_date, adults,isAnalysiss=False,hotelstarAnalysis=[],
                 priorityTimestamp=1,
                 use_cache=True):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        # self.isAnalysis=isAnalysiss
        self.isAnalysis=isAnalysiss[0] if isAnalysiss is tuple else isAnalysiss ,
        self.isAnalysis = self.isAnalysis[0] if isinstance(self.isAnalysis, tuple) else self.isAnalysis


        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp = priorityTimestamp
        self.use_cache = use_cache



        self.cookies = []

    def get_rooms(self,hotelCod, start_date, stay):
        params = {
            'hotelCod': hotelCod,
            'start_date': start_date,
            'stay': stay,
            'priorityTimestamp': self.priorityTimestamp,
            'use_cache': self.use_cache
        }

        base_url = settings.PROVIDER_SERVICES['ALAEDIN']['BASE_URL']
        endpoint = settings.PROVIDER_SERVICES['ALAEDIN']['ENDPOINTS']['ROOMS']
        response = requests.get(f"{base_url}{endpoint}", params=params, timeout=3600)

        json_data={}
        try:
            json_data = json.loads(response.text)['text']
            json_data=json.loads(json_data)
            json_data['room']
        except Exception as e:
            # print(f'in Getting json_data === {str(e)}')
            return []

        rooms = []
        for i in range(len(json_data['room'])):
            try:
                #==== Check karnae list entezar and etc
                if (hotelCod=='1226'):
                    print('ssd')
                if (json_data['room'][i]['isEntezar'] or
                        json_data['room'][i]['isNorozFr'] or
                        json_data['room'][i]['isViewPriceBoard']
                ):
                    # print(json_data['room'][i]['roomTypeName'])
                    continue
                #============

                room = {}
                room['name'] = json_data['room'][i]['roomTypeName']

                room['price'] = json_data['room'][i]['sumPrice']
                room['capacity']=json_data['room'][i]['numMax']
                room['provider'] = 'Alaedin'
                rooms.append(room)
            except Exception as e:
                print(f'in Getting rooms === {str(e)}')

        return rooms

    def get_hotels_info_writeJson(self):
        # Convert start and end dates
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
        stay_duration = (end_date - start_date).days
        shamsi_start_date = jdatetime.date.fromgregorian(date=start_date)
        shamsi_start_date_hotel = str(shamsi_start_date).replace("-", "")

        # Fetch hotel data
        url = f"https://www.alaedin.travel/hotels/{destin_text[self.target]}/{shamsi_start_date_hotel}/{stay_duration}"
        response = executeRequest(method="get", url=url,priorityTimestamp=self.priorityTimestamp)
        # response_data = response.json()
        response_data = json.loads(response)

        # Parse HTML response
        parser = etree.HTMLParser()
        html_parsed = etree.parse(StringIO(response_data["text"]), parser=parser)
        lst_hotels = html_parsed.xpath('//div[contains(@class,"hotel-box")]')

        res_lst_hotels = []
        hotel_futures = {}
        rooms_futures = {}

        # **Step 1: Parse hotel data in parallel**
        with ThreadPoolExecutor(max_workers=50) as hotel_executor:
            for hotel in lst_hotels:
                future = hotel_executor.submit(self.parse_hotel, hotel)
                hotel_futures[future] = hotel

        parsed_hotels = []
        for future in as_completed(hotel_futures):
            hotel_data = future.result()
            if hotel_data:
                parsed_hotels.append(hotel_data)

        # ------------ save hotesl into file

        if not os.path.exists('Alaedin_hotels'):
            os.makedirs('Alaedin_hotels')  # Creates the folder

        json.dump(parsed_hotels, open(f'Alaedin_hotels/Alaedin_hotel_info_{self.target}.json', 'w'))

        # --------------


    def get_result(self):
        try:

            # Convert start and end dates
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
            stay_duration = (end_date - start_date).days
            shamsi_start_date = jdatetime.date.fromgregorian(date=start_date)
            shamsi_start_date_hotel = str(shamsi_start_date).replace("-", "")
            res_lst_hotels = []
            hotel_futures = {}
            rooms_futures = {}
            #---- Load hotels info from Json
            with open(f'Alaedin_hotels/Alaedin_hotel_info_{self.target}.json','r') as f:
                a=f.read()
                parsed_hotels=json.loads(a)
            #--------------

            # ======== Check for hotel names or star ratings
            if self.isAnalysis:
                # Create a set of all hotel names for faster lookup
                all_hotel_names = {hotel['hotel_name'] for hotel in parsed_hotels}
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
                    parsed_hotels = [hotel for hotel in parsed_hotels if hotel['hotel_name'] in selected_hotels]
                else:
                    # Fallback to original star rating and name check
                    parsed_hotels = [hotel for hotel in parsed_hotels
                                   if (str(hotel['hotel_star']) in self.hotelstarAnalysis)
                                   or (hotel['hotel_name'] in self.hotelstarAnalysis)]

                print(f'Alaedin Analysis')
            else:
                print(f'Alaedin RASII')

            # ============


            # **Step 2: Fetch rooms in parallel**
            with ThreadPoolExecutor(max_workers=min(len(parsed_hotels),50)) as rooms_executor:
                for hotel_data in parsed_hotels:
                    future = rooms_executor.submit(
                        self.get_rooms, hotel_data["hotel_code"], str(shamsi_start_date), stay_duration
                    )
                    rooms_futures[future] = hotel_data

                for future in as_completed(rooms_futures):
                    hotel_data = rooms_futures[future]
                    try:
                        hotel_data["rooms"] = future.result()
                    except Exception as exc:
                        print(f"Error fetching rooms for {hotel_data['hotel_name']}: {exc}")
                        continue

                    # Convert Rial to Toman
                    for room in hotel_data["rooms"]:
                        room["price"] = str(int(room["price"]))[:-1]

                    res_lst_hotels.append(hotel_data)

            return res_lst_hotels

        except Exception as e:
            print(f"Error: {e}")
            return {"status": False, "data": [], "message": "اتمام زمان"}

    # **Helper Function for Parsing Hotel Data**
    def parse_hotel(self, hotel):
        try:
            hotel_name = hotel.xpath('.//div[@class="hotel-name"]/text()')[0]
            hotel_star = len(hotel.xpath('.//div[@class="hotel-star"]/i[contains(@class,"ala-color-yellow")]'))

            hotel_code = hotel.xpath('.//input[@class="hotelCode"]')[0].get("value")

            try:
                hotel_rial = hotel.xpath('.//div[@class="hotel-price text-center"]//small[text()="ریال"]')[0].text
            except:
                return None  # Skip hotels without a price

            return {
                "hotel_name": hotel_name,
                "hotel_code": hotel_code,
                "hotel_star": hotel_star,
                "min_price": "",
                "provider": "Alaedin",
                "rooms": [],
            }
        except Exception as e:
            print(f"Error parsing hotel: {e}")
            return None

    def get_result_OLD(self):
        try:

            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            shamsi_start_date = jdatetime.date.fromgregorian(date=start_date)
            shamsi_start_date_hotel=str(shamsi_start_date).replace('-','')

            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            stay_duration = (end_date - start_date).days

            # aa = requests.get('https://www.alaedin.travel/hotels/kish/14030803/3')
            # aa = requests.get(f'https://www.alaedin.travel/hotels/{self.destin_text[self.target]}/{shamsi_start_date_hotel}/{stay_duration}',timeout=3600)
            aa = executeRequest(method='get',
                url=f'https://www.alaedin.travel/hotels/{destin_text[self.target]}/{shamsi_start_date_hotel}/{stay_duration}',
                                priorityTimestamp=self.priorityTimestamp)
            # aa=aa.json()
            aa = json.loads(aa)


            # ==parsing
            parser = etree.HTMLParser()
            htmlparsed = etree.parse(StringIO(aa['text']), parser=parser)
            lst_hotels = htmlparsed.xpath('//div[contains(@class,"hotel-box")]')
            res_lst_hotels = list()
            with ThreadPoolExecutor(max_workers=100) as executor:
                future_to_hotel = {}
                for hotel in lst_hotels:
                    hotelName = hotel.xpath('.//div[@class="hotel-name"]/text()')[0]
                    hotelCode = hotel.xpath('.//input[@class="hotelCode"]')[0].get('value')
                    # hotelHref='https://www.alaedin.travel'+hotel.xpath('./../@href')[0]
                    try:
                        hotelRial=hotel.xpath('.//div[@class="hotel-price text-center"]//small[text()="ریال"]')[0].text
                    except:
                        continue  # yani gheymat nadarad!!


                    hotel_data = {}
                    hotel_data['hotel_name'] =hotelName
                    hotel_data['hotel_star'] = ''
                    hotel_data['min_price'] =''
                    hotel_data['provider'] = 'Alaedin'
                    hotel_data['rooms'] = []
                    # == get rooms
                    future = executor.submit(self.get_rooms, hotelCode, str(shamsi_start_date), stay_duration)
                    future_to_hotel[future] = hotel_data  # Keep track of hotel data

                # Collect results as they complete
                for future in as_completed(future_to_hotel):
                    hotel_data = future_to_hotel[future]
                    try:
                        hotel_data['rooms'] = future.result()  # Get the result from the future
                    except Exception as exc:
                        print(f'Alaeddin Error fetching rooms for {hotel_data["hotel_name"]}: {exc}')
                        continue

                    #===
                    # Convert Rial to Toman
                    #===

                    for room in hotel_data['rooms']:
                        room['price']=str(int( room['price']))[:-1]

                    #====


                    res_lst_hotels.append(hotel_data)

            return res_lst_hotels

        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}


# === for first time = (create hotel info )
from datetime import datetime,timedelta
# with open(f'Booking_hotel_info_{self.target}.json','r') as f:
lst_targets1=list(destin_text.keys())
start_date1 = datetime.today() + timedelta(days=4)
start_date1 = start_date1.strftime("%Y-%m-%d")

end_date1 = datetime.today() + timedelta(days=7)
end_date1 = end_date1.strftime("%Y-%m-%d")

isAnalysiss = False
adults = '2'
import concurrent.futures

for tg in lst_targets1:
    if os.path.exists(f'Alaedin_hotels/Alaedin_hotel_info_{tg}.json'):
        ''
    else:
        ins = Alaedin(tg, start_date1, end_date1, adults, isAnalysiss, hotelstarAnalysis=[])
        ins.get_hotels_info_writeJson()
        print(f'Alaedin_hotels/Alaedin_hotel_info_{tg}.json  is created!')

# =================



    #
    # hotel = {}
    # hotel['hotel_name'] = ''
    # hotel['hotel_star'] = ''
    # hotel['min_price'] = ''
    # hotel['provider'] = ''
    # hotel['rooms'] = [
    #     {
    #         'name': '',
    #         'price': '',
    #         'provider': '',
    #     }
    # ]
    # pass

#
# #=== Alaedin ===
#
# Alaedin=Alaedin('KIH','2024-10-30','2024-11-04','2')
# Alaedin.get_result()
# #===========
