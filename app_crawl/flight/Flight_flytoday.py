import pandas as pd
file_path = 'app_crawl/flight/Bansard-airlines-codes-IATA-ICAO.xlsx'
# Read the Excel file
df = pd.read_excel(file_path)
iata_to_airline = dict(zip(df['IATA Designator'], df['Airline Name']))


#------ Flight ---
import requests
import json
import jdatetime
class FlyToDay:
    def __init__(self, start_date,source, target):
        self.start_date = start_date
        # self.persian_start_date = convert_gregorian_date_to_persian(start_date)['date']
        # self.end_date = end_date
        self.source = source
        self.target = target
    def get_result(self):

        headers = {
            'accept': '*/*',
            'accept-language': 'fa-IR',
            'authorization': 'Bearer null',
            'cache-control': 'max-age=0',
            'content-type': 'application/json',
            'origin': 'https://www.flytodayir.com',
            'priority': 'u=1, i',
            'referer': 'https://www.flytodayir.com/',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-app': 'www.flytodayir.com',
            'x-path': 'https://www.flytodayir.com/flight/search?departure=mhd,1&arrival=dxb,1&departureDate=2024-11-03&adt=1&chd=0&inf=0&cabin=1&isAnyWhere=false',
            # 'x-token': '3239736a37706a585678713569724c6b5379644c6e57386455476945497936686d48547357717931676c514c445035556d36646e4270486a616d586257457969',
        }

        json_data = {
            'pricingSourceType': 0,
            'adultCount': 2,
            'childCount': 0,
            'infantCount': 0,
            'travelPreference': {
                'cabinType': 'Y',
                'maxStopsQuantity': 'All',
                'airTripType': 'OneWay',
            },
            'originDestinationInformations': [
                {
                    # 'departureDateTime': '2024-11-03',
                    'departureDateTime': self.start_date,
                    # 'destinationLocationCode': 'DXB',
                    'destinationLocationCode': self.target,
                    'destinationType': 'City',
                    # 'originLocationCode': 'MHD',
                    'originLocationCode': self.source,
                    'originType': 'City',
                },
            ],
            'isJalali': True,
        }

        response = requests.post('https://api.flytoday.ir/api/V1/flight/search', headers=headers, json=json_data)
        flight_json=json.loads(response.text)

        #== parse flight
        provider_flight={
            'FZ':'',
            'G9':'',
            'TK':'Turkish'
        }
        from datetime import datetime
        lst_flights=[]
        flights=flight_json['pricedItineraries']
        for flightItem in flights:

            # -- departure time and time
            datetime_flight=flightItem['originDestinationOptions'][0]['flightSegments'][0]['departureDateTime']
            datetime_flight=datetime.fromisoformat(datetime_flight)
            date_flight=str(datetime_flight.date())
            # Split the string and create a datetime object
            year, month, day = map(int, date_flight.split('-'))
            jalali_date = jdatetime.date.fromgregorian(year=year, month=month, day=day)
            jalali_date=str(jalali_date).replace('-','/')


            #-- arical time and date
            datetime_flight2=flightItem['originDestinationOptions'][0]['flightSegments'][0]['arrivalDateTime']
            datetime_flight2=datetime.fromisoformat(datetime_flight2)
            date_flight2=str(datetime_flight2.date())
            # Split the string and create a datetime object
            year, month, day = map(int, date_flight2.split('-'))
            jalali_date2 = jdatetime.date.fromgregorian(year=year, month=month, day=day)
            jalali_date2=str(jalali_date2).replace('-','/')


            flight = {}

            flight['airline_code'] = flightItem['originDestinationOptions'][0]['flightSegments'][0]['operatingAirline']['code']
            flight['airline_name'] = iata_to_airline.get(flight['airline_code'],flight['airline_code'])
            flight['go_time'] = str(datetime_flight.time())[:5]
            flight['go_date'] = str(jalali_date)
            flight['return_time'] = str(datetime_flight2.time())[:5]
            flight['return_date'] =  str(jalali_date2)
            flight['flight_number'] = flightItem['originDestinationOptions'][0]['flightSegments'][0]['operatingAirline']['flightNumber']
            flight['provider_name'] = 'FlyToday'
            flight['provider_logo'] = 'https://s8.uupload.ir/files/flytoday_logo_xb1u.jpg'
            flight['price'] =int(str(flightItem['airItineraryPricingInfo']['itinTotalFare']['totalFare'])[:-1])/2
            flight['seat'] = '5'
            flight['buy_link'] = 'https://www.flytoday.ir'

            lst_flights.append(flight)

        return lst_flights


# fly = FlyToDay("2024-10-27", "MHD", "DXB")
# print("--------------------------------")
# print('result', fly.get_data())