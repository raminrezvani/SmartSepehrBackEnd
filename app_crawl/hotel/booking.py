import json
from concurrent.futures import ThreadPoolExecutor, wait
from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Booking:
    def __init__(self, target, start_date, end_date, adults,iter=iter):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.call_count = iter
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.url = f"https://www.booking.ir/fa/hotel/iran/{target.lower()}/?i={self.start_date}&o={self.end_date}&r=1;&n=ir&d=1640809&lt=1&dt=2&a=2&c=0#/"
        self.header = {
            'Content-Type': 'application/json'
        }

        self.static_session_id = ""
        self.cookies = []

    def get_result(self):
        try:
            #==========ssssssssss


            self.call_count+=1

            if (self.call_count<=3):
                #==========ssssssssss
                urll = "http://45.149.76.168:5002/booking_hotels"
            else:
                urll = "http://130.185.77.24:5002/booking_hotels"


            # urll = "http://45.149.76.168:5002/booking_hotels"


            params = {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'adults':self.adults,
                'target':self.target
            }
            response = requests.get(urll, params=params)
            data=response.json()
            #=============

            if len(data) <= 0:
                return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}

        result = data

        return result
