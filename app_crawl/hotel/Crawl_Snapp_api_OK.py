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

class Snapp:
    def __init__(self, target, start_date, end_date, adults):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.executor = ThreadPoolExecutor(max_workers=50)
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
            url = 'http://45.149.76.168:5004/SnappTrip_Hotelrooms'
            params = {
                # 'date_from': '2024-11-05',
                'date_from': start_date,
                # 'date_to': '2024-11-08',
                'date_to': end_date,
                'city_id':  self.city_id,
            }

            response = requests.get(url, params=params)
            res=json.loads(response.text)
            #-----------------------------
            return res

        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}





