import json
from concurrent.futures import ThreadPoolExecutor, wait
from app_crawl.helpers import convert_to_tooman
from requests import request
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import random
SERVER_ADD='http://localhost:3030/'
class Jimbo:
    def __init__(self, target, start_date, end_date,
                 adults,iterr=1,isAnalysiss=False,
                 hotelstarAnalysis=[],priorityTimestamp=1,
                 use_cache=True):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        # self.isAnalysis=isAnalysiss

        self.isAnalysis = isAnalysiss[0] if isAnalysiss is tuple else isAnalysiss,
        self.isAnalysis = self.isAnalysis[0] if isinstance(self.isAnalysis, tuple) else self.isAnalysis

        self.hotelstarAnalysis = hotelstarAnalysis
        self.priorityTimestamp = priorityTimestamp
        self.use_cache = use_cache


        self.call_count = iterr

        self.url = f"https://www.jimbo.ir/fa/hotel/iran/{target.lower()}/?i={self.start_date}&o={self.end_date}&r=1;&n=ir&d=1640809&lt=1&dt=2&a=2&c=0#/"
        self.header = {
            'Content-Type': 'application/json'
        }

        self.static_session_id = ""
        self.cookies = []

    def get_result(self):
        try:


            self.call_count+=1
            #
            # if (self.call_count<=1000):
            #     #==========ssssssssss
            #     # ports =  [5020,5021]
            #     ports = [6060]
            #     # Use round-robin selection
            #     selected_port = ports[self.call_count % len(ports)]
            #
            #     urll = f"http://45.149.76.168:{selected_port}/Jimbo_hotels"
            #
            # else:
            #     urll = "http://130.185.77.24:5020/Jimbo_hotels"



            #==========ssssssssss
            # urll = "http://45.149.76.168:5020/Jimbo_hotels"
            urll = SERVER_ADD + "Jimbo_hotels"

            params = {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'adults':self.adults,
                'target':self.target,
                'isAnalysis': '1' if self.isAnalysis else '0',
                'hotelstarAnalysis': json.dumps(self.hotelstarAnalysis),
                'priorityTimestamp': self.priorityTimestamp,
                'use_cache': self.use_cache
            }
            response = requests.get(urll, params=params)
            # data=response.json()
            data=json.loads(response.text)

            #=============

            if len(data) <= 0:
                return {'status': False, 'data': [], 'message': "داده ای یافت نشد"}
        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}

        result = data

        return result
