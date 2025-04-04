import json
from concurrent.futures import ThreadPoolExecutor, wait
from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3
import requests
from datetime import datetime
from app_crawl.hotel.Client_Dispatch_requests import executeRequest

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SERVER_ADD='http://localhost:8022/'

class Eghamat24:
    def __init__(self, target, start_date, end_date, adults,isAnalysiss=False,
                 hotelstarAnalysis=[],priorityTimestamp=1,
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

        self.header = {
            'Content-Type': 'application/json'
        }

        self.static_session_id = ""
        self.cookies = []

    def get_result(self):
        try:
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            stay_duration = (end_date - start_date).days

            #==========ssssssssss

            urll = SERVER_ADD+"fetch_hotels"
            params = {
                'target': self.target,
                'startdate': self.start_date,
                'stay': stay_duration,
                'isAnalysis': '1' if self.isAnalysis else '0',
                'hotelstarAnalysis':json.dumps(self.hotelstarAnalysis),
                'priorityTimestamp':self.priorityTimestamp,
                'use_cache': self.use_cache

            }
            response = requests.get(urll, params=params)
            data=response.json()
            # data = json.loads(response)
            #=============

            if len(data) <= 0:
                return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}

        result = data

        return result
