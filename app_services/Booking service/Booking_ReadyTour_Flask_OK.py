import os
import json
import time
from threading import Thread
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
import traceback
from app_crawl.hotel.Client_Dispatch_requests import executeRequest

# Initialize Flask app
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=200)

# Set window title
os.system("title Booking Ready Tour Flask")


base_url = "https://www.booking.ir"
cookies_file = "Booking_readyTour_cookies.json"
def create_cookie_with_selenium() -> None:
    """Create and save authentication cookies using Selenium"""
    try:
        driver = webdriver.Chrome()
        driver.get(f'{base_url}/sign-in/')
        print('Signing in...')

        mobile_input = driver.find_element(By.XPATH, '//input[@id="Mobile"]')
        mobile_input.clear()
        mobile_input.send_keys('09153148721')

        driver.find_element(By.XPATH, '//span[contains(text(),"ورود با رمز ثابت")]/..').click()
        time.sleep(1)

        password_input = driver.find_elements(By.XPATH, '//input[@placeholder="رمز عبور ثابت"]')[1]
        password_input.clear()
        password_input.send_keys('@MST8451030yf')

        driver.find_elements(By.XPATH, '//span[text()="ورود"]/..')[-1].click()
        time.sleep(1)

        while driver.current_url != f"{base_url}/account/companies/?returnUrl=/":
            time.sleep(1)

        driver.find_element(By.XPATH, '//button[contains(text(),"مجلل سفر طلایی")]').click()
        time.sleep(5)

        cookies = driver.get_cookies()
        with open(cookies_file, "w") as file:
            json.dump(cookies, file)
        print('Cookies saved successfully')

    except Exception as e:
        print(f'Error creating cookies: {e}')
    finally:
        driver.quit()

def _refresh_cookies_periodically():
    """Refresh cookies every 3 hours"""
    while True:

        if os.path.exists(cookies_file):
            time.sleep(3 * 60 * 60)  # 3 hours
            os.remove(cookies_file)

        create_cookie_with_selenium()
        time.sleep(3 * 60 * 60)  # 3 hours


# Start cookie refresh thread
cookie_thread = Thread(target=_refresh_cookies_periodically)
cookie_thread.daemon = True
cookie_thread.start()


class BookingTour:
    def __init__(self,source,target,start_date,night_count,adults):
        self.cookies_file = "Booking_readyTour_cookies.json"
        self.base_url = "https://www.booking.ir"
        self.city_mapping = {
            'MHD': '1640810', 'THR': '1641221', 'KIH': '1640809',
            'SYZ': '1640811', 'GSM': '1640807', 'IFN': '1640808',
            'AZD': '1640806', 'TBZ': '1640812'
        }

        # # Initialize cookies if not exists
        # if not os.path.exists(self.cookies_file):
        #     create_cookie_with_selenium()



        self.source=source
        self.target = target
        self.adults=adults
        self.night_count=night_count

        self.start_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        self.end_date = (datetime.strptime(self.start_date, "%Y-%m-%d") + timedelta(days=self.night_count)).strftime("%Y-%m-%d")

        self.source_id = self.city_mapping.get(self.source, '')
        self.target_id = self.city_mapping.get(self.target, '')

        url = f"{self.base_url}/trip/?i={self.start_date}&o={self.end_date}&r=1&n=&d={self.target_id}&or={self.source_id}&a={self.adults}&c=0#/"
        self.cookies = self.load_cookies()
        self.session_id = self.get_session_id(url, self.cookies)



    def load_cookies(self) -> List[Dict]:
        """Load cookies from file"""
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, 'r') as json_file:
                return json.load(json_file)
        print(f'{self.cookies_file} not found!')
        return ''

    @staticmethod
    def convert_persian_number_to_english(number: str) -> str:
        """Convert Persian numbers to English"""
        numbers = {"۱": "1", "۲": "2", "۳": "3", "۴": "4", "۵": "5",
                   "۶": "6", "۷": "7", "۸": "8", "۹": "9", "۰": "0"}
        return "".join(numbers.get(num, num) for num in number)

    def clean_price(self, price: str) -> str:
        """Clean price string and convert to English numbers"""
        price = price.replace(',', '').replace('ريال', '').strip()
        return self.convert_persian_number_to_english(price)

    def get_session_id(self, url: str, cookies: List[Dict]) -> str:
        """Get session ID from initial request"""
        headers = {"Cookie": "; ".join(f"{c['name']}={c['value']}" for c in cookies)}
        while True:
            try:
                req = requests.get(url, headers=headers, timeout=10)
                if req.status_code == 200:
                    return req.text.split('sessionId')[1].split(',"basic"')[0].replace(':', '').replace('"', '')
                print(f'Cookie error - Status: {req.status_code}')
                # cookies = self.create_cookie_with_selenium()
                # headers["Cookie"] = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
            except requests.RequestException as e:
                print(f'Request failed: {e}')
                time.sleep(1)

    def parse_results(self, json_data: Dict) -> List[Dict]:
        """Parse tour results from JSON response"""
        results = []
        try:
            hotel_itineraries = json_data['model']['hotelBookingSearchResult']['hotelBookingItineraries']

            for itinerary in hotel_itineraries:
                go_flight = {
                    "price": None,
                    "departure_time": None,
                    "airline": itinerary['flightItineraries'][0]['flights'][0]['flightsSegments'][0][
                        'operatingAirlineTitle'],
                    "arrive_time": itinerary['flightItineraries'][0]['flights'][0]['departureDateTime']
                }
                return_flight = {
                    "price": None,
                    "departure_time": None,
                    "airline": itinerary['flightItineraries'][1]['flights'][0]['flightsSegments'][0][
                        'operatingAirlineTitle'],
                    "arrive_time": itinerary['flightItineraries'][1]['flights'][0]['departureDateTime']
                }

                results.append({
                    "hotel_name": itinerary['hotel']['title'],
                    "hotel_star": itinerary['hotel']['rating'],
                    "hotel_price": self.clean_price(str(itinerary['bestPackage']['totalPrice'])),
                    "total_price": self.clean_price(str(itinerary['bestPackage']['totalPrice'])),
                    "room_name": itinerary['bestPackage']['packages'][0]['rooms'][0]['roomTypeTitle'].strip(),
                    "go_flight": go_flight,
                    "return_flight": return_flight,
                    "system_provider": "booking"
                })
        except KeyError as e:
            print(f'Error parsing results: {e}')
        return results

    def get_tours(self) -> Dict:
        """Get booking tours data"""
        try:


            headers = {"Cookie": "; ".join(f"{c['name']}={c['value']}" for c in self.cookies)}


            req = executeRequest(method='get', url=f'{self.base_url}/v2/trip/searchpackage/?sessionid={self.session_id}',
                                 headers=headers,
                                 # priorityTimestamp=self.priorityTimestamp,
                                 use_cache=True)
                                 # forceGet=force)
            res = json.loads(req)

            # res = requests.get(f'{self.base_url}/v2/trip/searchpackage/?sessionid={self.session_id}'
            #                    ,
            #                    headers=headers, timeout=10)
            if res['status_code'] == 200:
                # json_res = json.loads(res['text'])
                # parsed_results = self.parse_results(json_res)
                # return {"status": "success", "data": parsed_results}
                return res
            return {"status": False, "message": f"Request failed with status: {res.status_code}"}

        except Exception as e:
            traceback.print_exc()
            return {"status": "error", "message": str(e)}


# Flask route
@app.route('/booking_tours', methods=['GET'])
def booking_tours():
    try:
        start_date = request.args.get('start_date')
        night_count = request.args.get('night_count', type=int)
        adults = request.args.get('adults', '2')
        source = request.args.get('source', 'MHD')
        target = request.args.get('target', 'KIH')

        if not start_date or not night_count:
            return jsonify({"error": "Missing start_date or night_count"}), 400

        booking = BookingTour(source,target,start_date,night_count,adults)
        future = executor.submit(booking.get_tours,)
        result = future.result()
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)