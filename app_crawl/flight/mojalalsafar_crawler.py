import requests
import jdatetime
import requests
from io import StringIO
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
def convert_gregorian_date_to_persian(date: str, template: str = "%Y-%m-%d") -> dict:
    """
    convert gregorian date to jalali
    :param date: format ==> YYYY-MM-DD
    :param template: output format
    :return: status, message, date
    """
    try:
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        return {
            "status": True,
            "message": "ok",
            "date": jdatetime.date.fromgregorian(year=year, month=month, day=day).strftime(template)
        }
    except:
        return {"status": False, "message": "something went wrong"}

def ready_price(price: str) -> str:
    """
    delete price noise
    :param price: str
    :return: price without noise
    """
    price = price.replace(',', '')
    price = price.replace('ريال', '')
    return convert_persian_number_to_english(price.strip())



def convert_persian_number_to_english(number: str):
    """
    check string if it has persian number, change it to english number
    :param number: any string
    :return:
    """
    numbers = {
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "۰": "0",
    }
    # ---
    result = [
        numbers[num] if num in list(numbers.keys()) else num for num in number
    ]
    # --- response
    return "".join(result)


dic_IATA={
    'MHD':'Mashhad',
    'THR':'Tehran',
    'KIH':'Kish',
    'GSM':'Gheshm',

    'SYZ': 'Shiraz',
    'IFN': 'Isfahan',
    'AZD': 'Yazd',
    'TBZ': 'Tabriz',


   'AWZ': 'Ahwaz',
   'BND': 'Bandar Abass',
   'ZBR': 'Chahbahar',
   'KER': 'Kerman',
   'KSH': 'Kermanshah',
   'RAS': 'Rasht',
   'SRY': 'Sari',
   'ABD': 'Abadan',
   'BUZ': 'Bushehr',
   'GBT': 'Gorgan',
   'OMH': 'Urmia',
   'ADU': 'Ardabil',
   'HDM': 'Hamedan',
   'RZR': 'Ramsar',
   'KHD': 'Khoramabad',
   'NSH': 'Noshahr',

# ===========
# ===========

}


class MojalalSafar():
    def __init__(self, start_date, end_date, source, target):
        self.start_date = convert_gregorian_date_to_persian(start_date, "%Y/%m/%d")['date'].replace('/','-')
        self.end_date = convert_gregorian_date_to_persian(end_date, "%Y/%m/%d")['date'].replace('/','-')
        self.source = source
        self.target = target
        self.post_header = {
            'Content-Type': 'application/json'
        }
        self.executor = ThreadPoolExecutor(max_workers=5)

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            # 'cookie': 'galaxy_ver=1.2.17; mojalalsafar.ir=OK; PHPSESSID=vbqe3van0ehise5q9m17r74b61; bl1=1; LastSeaarch=Mashhad%28MHD%29%D9%85%D8%B4%D9%87%D8%AF%7C10001%7CKish%28KIH%29%DA%A9%DB%8C%D8%B4%7C10003; __arcsco=1350686570cfad40631efab2cc864fc9',
            'priority': 'u=0, i',
            'referer': 'https://mojalalsafar.ir/Ticket-Mashhad-Kish.html?t=1403-06-06',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }

        self.params_start = {
            't': '',
        }
        self.params_end = {
            't': '',
        }

    def get_go_flight(self):

        self.params_start['t']=self.start_date
        response = requests.get(f'https://mojalalsafar.ir/Ticket-{dic_IATA[self.source]}-{dic_IATA[self.target]}.html?t={ self.params_start["t"]}', params=self.params_start, headers=self.headers)
        res = response.text

        parser = etree.HTMLParser()
        htmlparser = etree.parse(StringIO(res), parser=parser)
        lst_results = htmlparser.xpath('//*[@id="tab_record"]/div[@class="resu "]')
        result=[]
        for flight in lst_results:
            try:
                price = flight.xpath('.//div[@class="price "]/span')[0].text
                price=f'{price.replace(",","")}000'
                departureTime = flight.xpath('.//div[@class="date"]')[0].text.replace('\r', '').replace('\n',
                                                                                                        '').strip()
                airline = flight.xpath('.//img[@class="plan_icon"]')[1].get('rel')
                flight_number = flight.xpath('.//span[@class="code_inn"]')[0].text


                seat=flight.xpath('.//div[@class="user"]//text()')[1].replace('\r','').replace('\n','').strip().replace('+','')



                print(f'price == {price} departureTime == {departureTime}  airline== {airline} sear =={seat}')

                if ('Zagros' in airline):
                    airline_name="زاگرس"
                    airline_code="ZV"
                else:
                    airline_name=airline.split('_ok.png')[0]
                    airline_code=airline.split('_ok.png')[0]

                result.append({
                    "airline_name": airline_name,
                    "airline_code": airline_code,
                    "go_time": departureTime,
                    "go_date": self.start_date.replace('-','/'),
                    "return_time": "",
                    "return_date": "",
                    "flight_number": flight_number,
                    "provider_name": "مجلل سفر طلایی",
                    # "provider_logo": "https://cdn.charter725.ir/template/backc118/../../uploads/mojalalsafar.ir/lange_logo_1582653509.jpg",
                    "provider_logo": "https://s8.uupload.ir/files/logo_mojalal_zqs9.png",
                    "price": int(ready_price(price)),
                    "seat": str(seat),
                    "buy_link": 'https://www.mojalalsafar.ir'
                })



            except:
                continue
        # ---
        return result

    def get_return_flight(self):

        self.params_end['t']=self.end_date
        # response = requests.get('https://mojalalsafar.ir/Ticket-Kish-Mashhad.html', params=self.params, headers=self.headers)
        response = requests.get(f'https://mojalalsafar.ir/Ticket-{dic_IATA[self.target]}-{dic_IATA[self.source]}.html', params=self.params_end, headers=self.headers)

        res = response.text

        parser = etree.HTMLParser()
        htmlparser = etree.parse(StringIO(res), parser=parser)
        lst_results = htmlparser.xpath('//*[@id="tab_record"]/div[@class="resu "]')
        result=[]
        for flight in lst_results:
            try:
                price = flight.xpath('.//div[@class="price "]/span')[0].text
                price=f'{price.replace(",","")}000'
                departureTime = flight.xpath('.//div[@class="date"]')[0].text.replace('\r', '').replace('\n',
                                                                                                        '').strip()
                airline = flight.xpath('.//img[@class="plan_icon"]')[1].get('rel')
                flight_number =flight.xpath('.//span[@class="code_inn"]')[0].text


                seat=flight.xpath('.//div[@class="user"]//text()')[1].replace('\r','').replace('\n','').strip().replace('+','')



                print(f'price == {price} departureTime == {departureTime}  airline== {airline} sear =={seat}')
                if ('Zagros' in airline):
                    airline_name = "زاگرس"
                    airline_code = "ZV"
                else:
                    airline_name=airline.split('_ok.png')[0]
                    airline_code=airline.split('_ok.png')[0]

                result.append({
                    "airline_name":airline_name,
                    "airline_code":airline_code,
                    "go_time": departureTime,
                    "go_date": self.end_date.replace('-','/'),
                    "return_time": "",
                    "return_date":"",
                    "flight_number": flight_number,
                    "provider_name": "مجلل سفر طلایی",
                    # "provider_logo": "https://cdn.charter725.ir/template/backc118/../../uploads/mojalalsafar.ir/lange_logo_1582653509.jpg",
                    "provider_logo": "https://s8.uupload.ir/files/logo_mojalal_zqs9.png",
                    "price": int(ready_price(price)),
                    "seat": str(seat),
                    "buy_link": 'https://www.mojalalsafar.ir'
                })



            except:
                continue
        # ---
        # ---
        return result
    def get_result(self, one_way=True):
        try:
            result = dict()
            go_flight = self.executor.submit(self.get_go_flight)
            if not one_way:
                return_flight = self.executor.submit(self.get_return_flight)
                result['go_flight'] = go_flight.result()
                result['return_flight'] = return_flight.result()
            else:
                result = go_flight.result()
            # ---
            return result
        except:
            return {"go_flight": [], "return_flight": []} if not one_way else []


# mj=MojalalSafar("2024-08-27", "2024-08-27", "MHD", "KIH")
# aa=mj.get_result(one_way=False)

# sepehr = Sepehr360("2023-01-29", "2023-02-06", "MHD", "KIH")
# print("--------------------------------")
# print(sepehr.get_result())

