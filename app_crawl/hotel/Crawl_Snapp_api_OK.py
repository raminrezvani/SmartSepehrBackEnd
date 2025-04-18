#mojalalsafarmhd@gmail.com
#Mo@123456
from concurrent.futures import ThreadPoolExecutor, wait,as_completed
import urllib3
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import jdatetime
from lxml import etree
from io import StringIO
import requests
from django.conf import settings

class Snapp:
    def __init__(self, target, start_date, end_date, adults,isAnalysis=False,hotelstarAnalysis=[],
                 priorityTimestamp=1,
                 use_cache=True):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        # self.isAnalysis=isAnalysiss
        self.isAnalysis=isAnalysis[0] if isAnalysis is tuple else isAnalysis ,
        self.isAnalysis = self.isAnalysis[0] if isinstance(self.isAnalysis, tuple) else self.isAnalysis

        self.hotelstarAnalysis=hotelstarAnalysis
        self.priorityTimestamp = priorityTimestamp
        self.use_cache=use_cache
        self.cookies = []
        self.cityIDs={
            'KIH':'6918',
            'THR':'6433',
            'IFN':'6326',
            'MHD':'6497',
            'TBZ':'6220',
            'SYZ':'6640',
            'GSM':'6931',
            'AZD':'6969',
            'AWZ':'6541',
            'BND':'6926',
            'KER':'6713',
            'KSH':'6745',
            'RAS':'6814',
            'SRY':'6870',
            'ZBR':'6604',


            # =========
            'ABD':'6549',
            'BUZ':'6390',
            'GBT':'6782',
            'OMH':'6264',
            'ADU':'6288',
            'HDM':'6956',
            'RZR':'6857',
            'KHD':'6839',
            'NSH':'6865',
            #===========






        }

    def get_result(self):
        try:
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            shamsi_start_date = jdatetime.date.fromgregorian(date=start_date)
            shamsi_start_date_hotel=str(shamsi_start_date).replace('-','')
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            stay_duration = (end_date - start_date).days
            self.city_id=self.cityIDs[self.target]

            #--------- Get from Server ------------

            base_url = settings.PROVIDER_SERVICES['SNAPP']['BASE_URL']
            endpoint = settings.PROVIDER_SERVICES['SNAPP']['ENDPOINTS']['HOTELS']
            url = base_url + endpoint

            params = {
                'date_from': start_date,
                'date_to': end_date,
                'city_id': self.city_id,
                'target': self.target,
                'isAnalysis': '1' if self.isAnalysis else '0',
                'hotelstarAnalysis': json.dumps(self.hotelstarAnalysis),
                'priorityTimestamp': self.priorityTimestamp,
                'use_cache': self.use_cache
            }

            response = requests.get(url, params=params)
            # res=json.loads(response.text)

            #===
            res = json.loads(response.text)
            # res = json.loads(res )
            #===

            #-----------------------------
            return res

        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}





