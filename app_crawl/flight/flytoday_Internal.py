import json
from app_crawl.helpers import convert_to_tooman, convert_airlines, ready_price, convert_gregorian_date_to_persian

import requests


class FlyToDay:
    def __init__(self, start_date, end_date, source, target):
        self.start_date = start_date
        self.persian_start_date = convert_gregorian_date_to_persian(start_date)['date']
        self.end_date = end_date
        self.source = source
        self.target = target

    def get_data(self):
        # try:
        headers = {
            'authority': 'www.flytoday.ir',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': 'whitelabel_sid=nyanywogcwnattvfewzq2a0z; __RequestVerificationToken=0CjaDOVgAMx4QFaivdwsYF8HqEfHOqBaiFnE238dyNwurh5X2JBNbWgNNzpJvPobSfLQJMOo4BduvEHRHKvQeL7tqts1; _gcl_au=1.1.80100421.1674646817; analytics_campaign={%22source%22:%22sepehr360.ir%22%2C%22medium%22:%22referral%22}; analytics_token=055f8575-9b5c-112a-43e0-dc95ff7df47c; analytics_session_token=45b43e98-ecbc-d300-bcf3-2a2c63bcbd3e; yektanet_session_last_activity=1/25/2023; _yngt_iframe=1; _yngt=381afd4c-1eed-4f68-ac00-4813c3153525; _gid=GA1.2.1825025504.1674646818; _62c6a22d878dfd42d1279862=true; _ga=GA1.2.782671613.1674646817; _gat_UA-110464243-2=1; _ga_YXB24VE45D=GS1.1.1674646817.1.1.1674646901.39.0.0',
            'origin': 'https://www.flytoday.ir',
            'referer': 'https://www.flytoday.ir/flight/search?departure=MHD,1&arrival=KIH,1&departureDate=2023-01-30&adt=1&chd=0&inf=0&cabin=1',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'ReturnUrl': '',
            'OriginLocationCodes[0]': f'{self.source},1',
            'DestinationLocationCodes[0]': f'{self.target},1',
            'DepartureDateTimes[0]': self.persian_start_date,
            'DepartureDateTimes_Lang[0]': '',
            'AdultCount': '1',
            'ChildCount': '0',
            'InfantCount': '0',
            'CabinType': '1',
            '__RequestVerificationToken': 'OSoVEIQoPZq76dCz0ltZIufFtDJpHh1W6vKKYlYpsoPQ-xvvxighkecTBpsP-TiI0uf-v_7BhW49ht01_oKTsTfSUCs1',
            'Domestic': '',
            'Domestic_FlightType': 'OneWay',
            'StepDays': '0',
        }

        response = requests.post('https://www.flytoday.ir/flight/search/searchAjax', headers=headers, data=data)
        print("--------------------------------")
        print('text', response.text)
        data = json.loads(response.text)
        return [
            {
                "airline_name": convert_airlines(flight['DataAttribute']['Airlines']),
                "go_time": flight['FlightSegments'][0]['DepartureTimeString'],
                "go_date": self.start_date,
                "return_time": flight['ArrivalTimeString'][0]['ArrivalTimeString'],
                "return_date": self.end_date,
                "flight_number": flight['FlightSegments'][0]['FlightNumber'],
                "price": convert_to_tooman(
                    ready_price(flight['PtcFareBreakdowns'][0]['TotalFareWithMarkupAndVat'])),
                "seat": flight['FlightSegments'][0]['SeatsRemaining'],
                "providers": [{
                    "provider_name": "فلای تودی",
                    "price": convert_to_tooman(
                        ready_price(flight['PtcFareBreakdowns'][0]['TotalFareWithMarkupAndVat'])),
                    "seat": flight['FlightSegments'][0]['SeatsRemaining'],
                    "buy_link": f'https://www.flytoday.ir/flight/search?departure={self.source},1&arrival={self.target},1&departureDate={self.start_date}&adt=1&chd=0&inf=0&cabin=1'
                }]
            } for flight in data['result']['PricedItineraries']
        ]
        # except:
        #     return {"status": "unsuccessful"}


fly = FlyToDay("2023-01-27", "2023-02-06", "MHD", "KIH")
print("--------------------------------")
print('result', fly.get_data())
