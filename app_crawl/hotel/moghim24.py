import requests
import json
from concurrent.futures import ThreadPoolExecutor, wait
from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Moghim24:
    def __init__(self, target, start_date, end_date, adults):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults

    def get_data(self):
        url = "http://130.185.77.24:5678/get_data"
        params = {
            "destination": self.target,
            "adult": self.adults,
            "startdate": self.start_date,
            "enddate":  self.end_date
        }

        # Make the GET request
        response = requests.get(url, params=params)
        return json.loads(response.text)


    def get_result(self):
        try:
            data = self.get_data()
            data=json.loads(data['value'])
            if not data['isSucceed']:
                return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}


        return data['data']

