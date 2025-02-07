import time

from requests import request
import json
from datetime import timedelta, datetime
from app_crawl.helpers import convert_to_tooman, convert_gregorian_date_to_persian
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Deltaban:
    def __init__(self, start_date, night_count,source, target, adults=2):
        end_date = datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=night_count)
        self.start_date = start_date
        self.night_count = night_count
        self.end_date = end_date.strftime("%Y-%m-%d")
        self.start_date_persian = convert_gregorian_date_to_persian(self.start_date)
        self.end_date_persian = convert_gregorian_date_to_persian(self.end_date)
        # self.source = "MHD"
        self.source = source
        self.destination = target
        self.adults = adults
        if target == "MHD":
            self.location_id = 401
        elif target == "GSM":
            self.location_id = 448

        elif target == "SYZ":
            self.location_id = 412
        elif target == "THR":
            self.location_id = 400
        elif target == "IFN":
            self.location_id = 399
        elif target == "AZD":
            self.location_id = 421
        elif target == "TBZ":
            self.location_id = 439
        else:
            self.location_id = 402


        self.login = {
            "username": "mojalal",  # default => deltaban_guest
            "password": "@MST8451030yf"  # default => guest
        }
        self.post_header = {
            'Content-Type': 'application/json',
            "authorization": "130200"
        }

    @staticmethod
    def change_time(time):
        return f"{time[:2]}:{time[2:]}"

    def get_authorization(self):
        url = "https://api.3click.ir/auth/Login"
        headers = {
            'provider-code': 'deltaban',
            'Content-Type': 'application/json',
        }

        response = request("POST", url, headers=headers, data=json.dumps(self.login), verify=False)

        if response.status_code == 502:
            return ''


        if response.status_code != 200:
            self.get_authorization()

        data = json.loads(response.text)

        access_token = f"JWT {data['access_token']}"

        self.post_header['authorization'] = access_token
        return access_token

    def get_token(self):
        result_token=self.get_authorization()

        #-----
        if (result_token==''):  # fail in get token
            return ''
        #---------

        body = json.dumps({
            "flight": {
                "childs": 0,
                "infant": 0,
                "adults": self.adults,
                "source": self.source,
                "destination": self.destination,
                "flightDate": self.start_date,
                "returnFlightDate": self.end_date,
                "flight_class": "1",
                "searchTour": ""
            },
            "hotel": {
                "lang": "fa",
                "locationId": self.location_id,
                "startDate": self.start_date,
                "endDate": self.end_date,
                "passengerCounts": [
                    {
                        "childrenAges": [],
                        "adultsCount": self.adults
                    }
                ],
                "scope": "local",
                "limit": 20,
                "skip": 0,
                "hotelId": 0,
                "sortValue": [
                    {
                        "propertyName": "price",
                        "isASC": True
                    }
                ],
                "pidIds": []
            }
        })
        # ---
        url = "https://api.3click.ir/api2/TourDynamic/GetSearchToken"
        self.post_header['timestamp'] = str(int(datetime.now().timestamp()))
        # ---
        req = request("POST", url, headers=self.post_header, data=body, verify=False)
        # ---
        if req.status_code != 200:
            self.get_token()
        else:
            data = json.loads(req.text)
            return data['token']

    def get_data(self):
        token = self.get_token()

        #----
        if (token==''):
            return {"status": False, "hotels": [], "go_flights": [],
                    "return_flights": [] , 'Message':'دریافت توکن مشکل دارد'}
        #-----



        counter = 0
        went_flight_id = ""
        return_flight_id = ""
        hotel_result = []
        while counter < 30:
            body = json.dumps({
                "wentFlightId": went_flight_id,
                "returnFlightId": return_flight_id,
                "token": token,
                "limit": 20,
                "skip": 0,
                "scope": "local",
                "sortValue": [
                    {
                        "propertyName": "price",
                        "isASC": True
                    }
                ]
            })
            # ---
            url = "https://api.3click.ir/api2/TourDynamic/GetSearchResult"
            self.post_header['timestamp'] = str(int(datetime.now().timestamp()))
            # ---
            req = request("POST", url, headers=self.post_header, data=body, verify=False)
            # ---
            if req.status_code == 200:
                data = json.loads(req.text)
                go_flights = data['wentFlight']
                return_flights = data['returnFlight']
                hotels = data['hotelsV2']
                try:
                    hotel_result.extend(hotels)
                except:
                    pass
                if data['isFinish']:
                    return {"status": True, "hotels": hotel_result, "go_flights": go_flights,
                            "return_flights": return_flights}
                    # return {"status": True, "hotels": data['hotelsV2'], "go_flights": go_flights,
                    #         "return_flights": return_flights}
                else:
                    if len(data['hotelsV2']) and (not went_flight_id or not return_flight_id):
                        if not went_flight_id:
                            try:
                                went_flight_id = go_flights['extras']['flight_id']
                            except:
                                pass
                        if not return_flight_id:
                            try:
                                return_flight_id = return_flights['extras']['flight_id']
                            except:
                                pass
            elif req.status_code == 401:
                return {"status": False,'Message':'خطای 401 '}
            # ---
            counter += 1
            time.sleep(0.2)
        # ---
        return {"status": True, "hotels": hotel_result, "go_flights": go_flights,
                "return_flights": return_flights}
        # return {"status": False}

    def get_result(self):
        # try:
        data = self.get_data()
        if not data['status']:
            return {'status': False, "data": [], "message": data['Message']}
        # except:
        #     return {'status': False, "data": [], "message": "اتمام زمان"}
        # ---

        # --- calc go flight
        try:
            go_flight = data['go_flights']
            go_flight = {
                "airline": go_flight['airlineDetail']['persianName'],
                "airline_english": go_flight['airlineDetail']['englishName'],
                "flight_number": go_flight['flight_num'],
                "departure_date": go_flight['departure_date'],
                "departure_time": self.change_time(go_flight['departs']),
                "arrive_time": self.change_time(go_flight['departs']),
                "agency": go_flight['persianAgencyCode'],
                "price": min([air['fee_without_discount'] for air in go_flight['classes']])
            }
        except:
            return {'status': False, "data": [], "message": "پرواز رفت یافت نشد"}
        # --- calc return flight
        try:
            return_flight = data['return_flights']
            return_flight = {
                "airline": return_flight['airlineDetail']['persianName'],
                "airline_english": return_flight['airlineDetail']['englishName'],
                "flight_number": return_flight['flight_num'],
                "departure_date": return_flight['departure_date'],
                "departure_time": self.change_time(return_flight['departs']),
                "arrive_time": self.change_time(return_flight['departs']),
                "agency": return_flight['persianAgencyCode'],
                "price": min([air['fee_without_discount'] for air in return_flight['classes']])
            }
        except:
            return {'status': False, "data": [], "message": "پرواز برگشت یافت نشد"}
        # --- calc hotels
        try:
            hotels = {}
            for hotel in data['hotels']:
                key = hotel['persianName']
                total_price = convert_to_tooman(
                    ((int(hotel['minimumPackagePrice']) / self.adults) + go_flight['price'] + return_flight[
                        'price']) * self.adults)
                appended_item = {
                    "hotel_english_name": hotel['englishName'],
                    "hotel_name": hotel['persianName'],
                    "hotel_star": round(hotel['star']),
                    "hotel_rooms": [room['name'] for room in hotel['roomOfPackageWithMinimumPrices']],
                    "room_name": hotel['roomOfPackageWithMinimumPrices'][0]['name'],
                    "hotel_price": int(hotel['minimumPackagePrice']),
                    "go_flight": go_flight,
                    "return_flight": return_flight,
                    "commission": 0,
                    "status": "تایید شده",
                    "total_price": total_price,
                    "system_provider": "deltaban",
                    "redirect_link": f"https://3click.ir/flight%2Bhotel/MHD-KIH/search?pCount=2&room=1&scope=l&flightType=2&room-0=2&flightClass=Y&adults=2&city=%DA%A9%DB%8C%D8%B4&id=402&flightDate={self.start_date_persian}&returnDate={self.end_date_persian}"
                }
                if key in list(hotels.keys()):
                    if total_price <= hotels[key].get('total_price', total_price):
                        hotels[key] = appended_item
                else:
                    hotels[key] = appended_item
            # hotels = [
            #     {
            #         "hotel_english_name": hotel['englishName'],
            #         "hotel_name": hotel['persianName'],
            #         "hotel_star": round(hotel['star']),
            #         "hotel_rooms": [room['name'] for room in hotel['roomOfPackageWithMinimumPrices']],
            #         "room_name": hotel['roomOfPackageWithMinimumPrices'][0]['name'],
            #         "hotel_price": int(hotel['minimumPackagePrice']),
            #         "go_flight": go_flight,
            #         "return_flight": return_flight,
            #         "commission": 0,
            #         "status": "تایید شده",
            #         "total_price": convert_to_tooman(
            #             ((int(hotel['minimumPackagePrice']) / self.adults) + go_flight['price'] + return_flight['price']) * self.adults),
            #         "system_provider": "deltaban",
            #         "redirect_link": f"https://3click.com/flight%2Bhotel/MHD-KIH/search?pCount=2&room=1&scope=l&flightType=2&room-0=2&flightClass=Y&adults=2&city=%DA%A9%DB%8C%D8%B4&id=402&flightDate={self.start_date_persian}&returnDate={self.end_date_persian}"
            #     } for hotel in data['hotels']
            # ]
            return {'status': True, 'data': list(hotels.values()), 'message': ''}
        except:
            return {'status': False, "data": [], "message": "هتل یافت نشد"}


# deltaban = Deltaban("2023-08-04", 3, adults=3)
# print("--------------------------------")
# print(deltaban.get_result())
