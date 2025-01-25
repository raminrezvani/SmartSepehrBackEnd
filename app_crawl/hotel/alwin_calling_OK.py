import json
from concurrent.futures import ThreadPoolExecutor, wait
from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3
import requests
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Alwin:
    def __init__(self, target, start_date, end_date, adults):
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.target = target

    def get_result(self):
        try:
            # start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            # end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            # stay_duration = (end_date - start_date).days

            # ==========ssssssssss

            urll = "http://45.149.76.168:5053/alwin_hotels"
            params = {

                'startdate': self.start_date,
                'end_date': self.end_date,
                'adults': self.adults,
                'target': self.target,

            }
            response = requests.get(urll, params=params)
            data = response.json()
            # =============

            # if len(data) <= 0:
            #     return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}

        result = data

        return result
