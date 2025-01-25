import requests
import jdatetime
from datetime import date,timedelta
import json
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://mojalalsafar.ir',
    'priority': 'u=1, i',
    'referer': 'https://mojalalsafar.ir/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

dic_city={
    'MHD':'10001',
    'THR':'10000',
    'KIH':'10003',
    'GSM':'10012',
    'SYZ':'10005',
    'IFN':'10002',
    'AZD':'10027',
    'TBZ':'10006',

    'AWZ': '10004',
    'BND': '10010',
    'ZBR': '10081',
    'KER': '10011',
    'KSH': '10007',
    'RAS': '10024',
    'SRY': '10016',
    'ABD': '10030',
    'BUZ': '10015',
    'GBT': '10033',
    'OMH': '10028',
    'ADU': '10014',
    'HDM': '10008',
    'RZR': '10188',
    'KHD': '10075',
    'NSH': '10013',


}


class MojalalSafarCalendar():
    def __init__(self,source,target,skip_month=0) -> None:
        # georgian_date = date.today() + relativedelta(months=skip_month)

        georgian_date = date.today() + timedelta(days=skip_month*31)



        self.source = source
        self.target = target
        self.start_date = jdatetime.date.fromgregorian(day=georgian_date.day, month=georgian_date.month,
                                                       year=georgian_date.year)

    
    def get_data(self, source, target,pdate) -> dict:
        try:
            try:
                if (pdate!=0):
                    data = {
                        'from': dic_city[source],
                        'to': dic_city[target],
                        'ajax_load': '1',
                        'pdate':str(pdate)
                    }
                else:
                    data = {
                        'from': dic_city[source],
                        'to': dic_city[target],
                        'ajax_load': '1',

                    }
            except:
                return ''

            response = requests.post('https://mojalalsafar.ir/get_query.html', headers=headers, data=data)
            res_mojalal=json.loads(response.text)
            res_calendar={}
            res_calendar['arrival']=list()
            for item in res_mojalal['result']:
                try:
                    calendarItem={}
                    calendarItem['price']=int(item['price'].replace('<span>','').replace('</span>','').replace('تومان','')\
                                    .replace(',','').strip())
                    calendarItem['date']=f'1403/{item["date_flight"]}'
                    calendarItem['day']=int(item["date_flight"].split('/')[1])
                    calendarItem['isMinPrice']=False
                    year, month, day = map(int, calendarItem['date'].split('/'))
                    jalali_date = jdatetime.date(year, month, day)
                    calendarItem['flightDate'] =str(jalali_date.togregorian().strftime('%Y-%m-%dT%H:%M:%S'))

                    res_calendar['arrival'].append(calendarItem)
                except:
                    ''

            return res_calendar

        except:
            return {}

    def get_result(self):

        #=== old =====
        # go_data = self.get_data(source=self.source, target=self.target)
        # return_data = self.get_data(source=self.target, target=self.source)
        #
        # return {
        #     "go": go_data.get("arrival", []),
        #     "return": return_data.get("arrival", []),
        # }
        #===============

        #==================== for 60 days ahead ==========
        merged_go_data=list()
        merged_return_data=list()

        lst_date_go=list()
        lst_date_return=list()
        for i in range(4):
            go_data = self.get_data(source=self.source, target=self.target,pdate=i)
            for item in go_data['arrival']:
                if (item['date'] not in lst_date_go):
                    lst_date_go.append(item['date'])
                    merged_go_data.append(item)
            # merged_go_data.extend(go_data['arrival'])

            return_data = self.get_data(source=self.target, target=self.source, pdate=i)
            for item in return_data['arrival']:
                if (item['date'] not in lst_date_return):
                    lst_date_return.append(item['date'])
                    merged_return_data.append(item)
            # merged_return_data.extend(return_data['arrival'])


            print('asdasd')

        return {
            "go":merged_go_data,
            "return": merged_return_data
        }
        #===============================




# #=== calling ===========
# source="MHD"
# target="KIH"
# skip_month=0
# # ---
# sepehr = MojalalSafarCalendar(source=source, target=target, skip_month=skip_month)
# res=sepehr.get_result()
