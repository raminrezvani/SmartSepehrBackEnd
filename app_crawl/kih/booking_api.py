import json
from datetime import datetime, timedelta
from requests import request
# from app_crawl.helpers import convert_to_tooman
# from app_crawl.cookie.cookie_data import BOOKING as booking_cookie
import urllib3
import requests
from app_crawl.hotel.Client_Dispatch_requests import executeRequest


# Add this import at the top with other imports
from django.conf import settings


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Booking:
    def __init__(self,source,target, start_date, night_count, adults=2,iter=iter):
        self.start_date = start_date
        date_obj = datetime.strptime(self.start_date, "%Y-%m-%d")
        next_day = date_obj - timedelta(days=1)
        self.start_date = next_day.strftime("%Y-%m-%d")

        end_date = (datetime.strptime(self.start_date, "%Y-%m-%d").date() + timedelta(days=night_count)).strftime("%Y-%m-%d")

        self.call_count = iter  # Initialize call counter
        self.source=source
        self.target=target

        self.night_count = night_count
        self.end_date = end_date
        self.adults = adults
        self.url = f"https://www.booking.ir/trip/?i={self.start_date}&o={self.end_date}&r=1&n=&d=1640809&or=1640810&a={adults}&c=0#/"
        self.cookies = []
        self.header = {
            'Content-Type': 'application/json',
            "Cookie": ""
        }

    # def get_basic_cookies(self):
    #     driver = get_driver()
    #     driver.get(self.url)
    #
    #     self.cookies = [f"{cookie['name']}={cookie['value']}" for cookie in driver.get_cookies()]
    #
    #     driver.close()

    # def get_authorization(self):
    #     self.get_basic_cookies()
    #     url = "https://www.booking.ir/fa/v2/signinbymobile/"
    #
    #     payload = 'mobile=09153148721&password=MST1231020'
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #
    #     req = request("POST", url, headers=headers, data=payload, verify=False)
    #
    #     cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]
    #
    #     self.cookies.extend(cookies)
    #     self.header['Cookie'] = '; '.join(self.cookies)
    #     return req.cookies.get_dict()

    def get_auth(self):
        url = "https://www.booking.ir/fa/v2/signinbymobile/"

        payload = 'mobile=09153148721&password=@MST8451030yf'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req = request("POST", url, headers=headers, data=payload, verify=False)

        cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

        self.cookies.extend(cookies)
        self.header['Cookie'] = '; '.join(self.cookies)
        headers['cookie'] = '; '.join(self.cookies)

        req = request("GET", "https://www.booking.ir/account/getcompanies/", headers=headers, verify=False)

        data = json.loads(req.text)

        company_id = data['model'][0]['id']

        data = F"id={company_id}"

        req = request("POST", "https://www.booking.ir/account/signinbycompany/", headers=headers, data=data)

        print("--------------------------------")
        print(req.text)

        cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

        self.cookies = []
        self.cookies.extend(cookies)
        self.header['cookie'] = '; '.join(self.cookies)

        return req.cookies

    def get_session_id(self):
        self.get_auth()
        req = request("GET", self.url, headers=self.header)

        if req.status_code != 200:
            self.get_session_id()

        req_text = req.text

        basic_index = req_text.find("basic")
        session_index = req_text.find('sessionId')

        session_id = req_text[session_index + 12:basic_index - 3]

        return session_id

    def get_data(self):
        url = f"https://www.booking.ir/trip/searchpackage/?sessionid={self.get_session_id()}"

        req = executeRequest(method='get',
                                  url=url,
                                  headers=self.header)
        #
        #                           priorityTimestamp=self.priorityTimestamp,
        #                           use_cache=self.use_cache)

        req=json.loads(req)



        # req = request("GET", url, headers=self.header)

        if req['status_code'] != 200:
            self.get_data()

        return json.loads(req['text'])

    def get_result(self):
        try:
            # Select server based on call count using settings
            server_url = (settings.PROVIDER_SERVICES['BOOKING_READYTOUR']['PRIMARY_SERVER'] 
                         if self.call_count <= settings.PROVIDER_SERVICES['BOOKING_READYTOUR']['THRESHOLD'] 
                         else settings.PROVIDER_SERVICES['BOOKING_READYTOUR']['SECONDARY_SERVER'])
            
            # Prepare request parameters
            params = {
                'start_date': self.start_date,
                'night_count': self.night_count,
                'adults': self.adults,
                'source': self.source,
                'target': self.target
            }
    
            # Make request with timeout and error handling
            try:
                response = requests.get(server_url, params=params, timeout=30)
                response.raise_for_status()  # Raise exception for bad status codes
                data = response.json()
                data = json.loads(data['text'])
            except (requests.RequestException, json.JSONDecodeError) as e:
                return {'status': False, "data": [], 'message': f"خطا در دریافت اطلاعات: {str(e)}"}
    
            if not data.get('isSucceed', False):
                return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
    
            # Extract flight and hotel data
            try:
                itineraries = data['model']['hotelBookingSearchResult']['hotelBookingItineraries']
                if not itineraries:
                    return {'status': False, 'data': [], 'message': "اطلاعات پرواز و هتل یافت نشد"}
    
                first_itinerary = itineraries[0]
                
                # Get go flight details
                go_flight = self._extract_flight_details(
                    first_itinerary['flightItineraries'][0]['flights'][0]
                )
                if not go_flight:
                    return {'status': False, "data": [], "message": "پرواز رفت یافت نشد"}
    
                # Get return flight details
                return_flight = self._extract_flight_details(
                    first_itinerary['flightItineraries'][1]['flights'][0]
                )
                if not return_flight:
                    return {'status': False, 'data': [], 'message': "پرواز برگشت یافت نشد"}
    
                # Process hotel results
                result = self._process_hotel_results(itineraries, go_flight, return_flight)
                return {"status": True, "data": result, 'message': ""}
    
            except Exception as e:
                return {'status': False, 'data': [], 'message': f"خطا در پردازش اطلاعات: {str(e)}"}
    
        except Exception as e:
            return {'status': False, "data": [], 'message': f"خطای سیستمی: {str(e)}"}
    
    def _extract_flight_details(self, flight_data):
        """Helper method to extract flight details"""
        try:
            departure_date = datetime.strptime(flight_data['departureDateTime'], '%Y-%m-%dT%H:%M:%S')
            return {
                "airline": flight_data['flightsSegments'][0]['airlineTitle'],
                "airline_english": flight_data['flightsSegments'][0]['airlineCode'],
                "flight_number": flight_data['flightsSegments'][0]['flightNumber'],
                "departure_date": departure_date.strftime("%Y-%m-%d"),
                "departure_time": departure_date.strftime("%H:%M"),
                "arrive_time": departure_date.strftime("%H:%M"),
                "price": 0
            }
        except:
            return None
    
    def _process_hotel_results(self, itineraries, go_flight, return_flight):
        """Helper method to process hotel results"""
        return [{
            "hotel_english_name": hotel['hotel']['slug'],
            "hotel_name": hotel['hotel']['title'],
            "hotel_star": hotel['hotel']['rating'],
            "hotel_rooms": [hotel['bestPackage']['packages'][0]['rooms'][0]['roomTypeTitle']],
            "room_name": hotel['bestPackage']['packages'][0]['rooms'][0]['roomTypeTitle'],
            "hotel_price": 0,
            "commission": 0,
            "status": "تایید شده",
            "go_flight": go_flight,
            "return_flight": return_flight,
            "total_price": int(hotel['bestPackage']['totalPrice']) / 10,
            "system_provider": "booking",
            "redirect_link": f"https://www.booking.ir/trip/?i={self.start_date}&o={self.end_date}&r=1&n=&a={self.adults}&c=0#/"
        } for hotel in itineraries]


# booking = Booking("2024-08-15", 3,)
# print("--------------------------------")
# print(booking.get_result())
