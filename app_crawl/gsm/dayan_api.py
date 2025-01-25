import os
import random
from pathlib import Path

from requests import request

from app_crawl.helpers import convert_gregorian_date_to_persian, ready_price, convert_to_tooman
from app_crawl.cookie.cookie_data import DAYAN as dayan_cookie
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = Path(__file__).resolve().parent


class Dayan:
    def __init__(self, start_date, night_count):
        start_date = convert_gregorian_date_to_persian(start_date, "%Y/%m/%d")['date']
        self.start_date = start_date
        self.night_count = night_count

    def get_data(self):
        gsm_cookie = dayan_cookie['GSM']
        cookies = dayan_cookie["GSM"]['cookie']
        rnd = random.randint(1550000000000000, 1560000000000009)

        headers = {
            'authority': dayan_cookie['domain'],
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://{dayan_cookie["domain"]}',
            'referer': f"https://{dayan_cookie['domain']}/Systems/FA/Reservation/Tour_NewReservation_Search2.aspx?action=display&rnd={rnd}",
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-microsoftajax': 'Delta=true',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'action': 'display',
            'rnd': rnd,
        }

        data = {
            'ScriptManager1': 'UpdatePanel1|btnSubmit',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': gsm_cookie['view_state'],
            '__VIEWSTATEGENERATOR': gsm_cookie['view_generator'],
            'dplFrom': 'MHD',
            'dplTo': 'GSM',
            'dplHotelName': '0',
            'txtDepartureDate': self.start_date,
            'dplNights': f"{self.night_count}",
            'dplAdult': '2',
            'dplChild': '0',
            'dplInfant': '0',
            'DepartureFlight': 'rptFlights_NonBackToBack$ctl02$rptFlight_Seats$ctl01$rdoFlight',
            'ReturningFlight': 'rptFlights_NonBackToBack$ctl04$rptFlight_Seats$ctl01$rdoFlight',
            '__ASYNCPOST': 'true',
            'btnSubmit': 'جستجو',
        }

        request(
            "POST",
            f"https://{dayan_cookie['domain']}/Systems/FA/Reservation/Tour_NewReservation_Search2.aspx",
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False
        )

        res = request(
            "GET",
            f"https://{dayan_cookie['domain']}/Systems/FA/Reservation/Tour_NewReservation_Search2.aspx?action=display&rnd={rnd}",
            cookies=cookies,
            verify=False
        )

        return res.text

    def get_static_data(self):
        with open('test.html', 'r') as html_file:
            data = html_file.read()
            html_file.close()
        return data

    def add_to_file(self, data):
        try:
            path_file = os.path.join(BASE_DIR, f'logs', f'dayan_{self.start_date.replace("/", "_")}.html')
            print("--------------------------------")
            print(path_file)
            with open(path_file, 'w', encoding="UTF-8") as html_file:
                html_file.write(data)
                # html_file.close()
            return True
        except:
            return False

    def get_result(self):
        try:
            data = self.get_data()

            soup = BeautifulSoup(data, 'html.parser')
            self.add_to_file(data)
            result = []
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}

        # --- go flight
        try:
            go_flight = soup.select_one('.df:has([name="DepartureFlight"]:checked)')
            go_price = go_flight.select_one('label').text.split(' ')
            go_price = ready_price(go_price[0])
            go_arrive = go_flight.select_one('td:nth-child(4)').text
            go_departure_time = go_flight.select_one('td:nth-child(5)').text
            go_airline = go_flight.select_one('td:nth-child(6)').text
            go_airline = go_airline.replace('\n', '').replace('\xa0\xa0\n', '')
            go_airline = go_airline.replace('737\n', '').replace('  ', '').strip().split(' ')[-1]
            go_flight = {
                "airline": go_airline,
                "arrive_time": go_arrive.strip(),
                "departure_time": go_departure_time.strip(),
                "price": go_price
            }
        except:
            return {'status': False, "data": [], "message": "پرواز رفت یافت نشد"}
        # --- return flight
        try:
            return_flight = soup.select_one(""".rf:has([name="ReturningFlight"]:checked)""")
            return_price = return_flight.select_one('label').text.split(' ')
            return_arrive = return_flight.select_one('td:nth-child(4)').text
            return_departure_time = return_flight.select_one('td:nth-child(5)').text
            return_airline = return_flight.select_one('td:nth-child(6)').text
            return_airline = return_airline.replace('\n', '').replace('\xa0\xa0\n', '')
            return_airline = return_airline.replace('737\n', '').replace('  ', '').strip().split(' ')[-1]
            return_flight = {
                "airline": return_airline,
                "arrive_time": return_arrive.strip(),
                "departure_time": return_departure_time.strip(),
                "price": ready_price(return_price[0])
            }
        except:
            return {'status': False, 'data': [], 'message': "پرواز برگشت یافت نشد"}
        # --- hotels
        try:
            hotels = soup.select("tr[bgcolor='#EEEEEE']")
            for hotel in hotels:
                hotel_name = hotel.select_one('label').text
                hotel_price_per_person = hotel.select_one('td:nth-child(2)').text
                hotel_room_name = hotel.select_one('td:nth-child(5)').text
                hotel_status = hotel.select_one('td:nth-child(6)').text
                # ---
                appended_data = {
                    "hotel_name": hotel_name,
                    "hotel_rooms": hotel_room_name,
                    "room_name": hotel_room_name,
                    "total_price": convert_to_tooman(int(ready_price(hotel_price_per_person)) * 2),
                    "commission": convert_to_tooman(int(ready_price(hotel.select_one('td:nth-child(3)').text))),
                    "go_flight": go_flight,
                    "return_flight": return_flight,
                    "status": hotel_status.strip(),
                    "system_provider": "dayan",
                    "redirect_link": f"https://{dayan_cookie['domain']}"
                }
                result.append(appended_data)

            # --- response
            return {'status': True, 'data': result, 'message': ""}
        except:
            return {'status': False, "data": [], 'message': "هتلی یافت نشد"}


# dayan = Dayan("2023-03-29", 3)
# print("--------------------------------")
# print(dayan.get_result())
