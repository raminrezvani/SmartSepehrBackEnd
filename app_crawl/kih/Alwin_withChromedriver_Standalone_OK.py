import datetime
from lxml import etree
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time
import json
from requests import request
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

#BASE_URL = "http://94.74.182.183:6886/"
BASE_URL = "http://localhost:6379/"
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from seleniumwire import webdriver  # Import from seleniumwire
import time
import jdatetime


# from app_crawl.helpers import convert_to_tooman, convert_airlines
from helpers import convert_to_tooman, convert_airlines
#from SepehrSmart.cache import add_cache
from cache.cache import add_cache








def has_key_cache(key: str) -> bool:
    """
    check if key has cache or not
    :param key: key
    :return: True => key has cache
    """
    try:
        key_exists = r.exists(key)

        return key_exists
    except:
        return False


def get_cache(key: str, get_time: bool = False) -> [list, dict]:
    """
    get cache data
    :param key: key
    :param get_time: get time of created
    :return: everything is in cache with the key
    """
    try:

        data = r.get(key)
        data=json.loads(data)

        return data
    except:
        return []


def add_cache(key: str, data: [list, dict]) -> bool:
    """
    add data to cache
    :param key: key
    :param data: data
    :return: True => data saved in cache, False => data cannot save in cache
    """
    try:

        print('Start caching...')

        aa=r.set(key, json.dumps(data))
        r.expire(key,15*60)
        # r.expire(key,30)
        if (aa):
            print('end caching SUCCESS')
        else:
            print('end caching Failed')
        return True

    except Exception as e:
        print(str(e))
        return False

def crawl_Allwin24_withSelenium(driver,startdayy,night,adults):



    while(True):
        try:
            # source, destination
            # Preprocess
            # startday='2027-07-10'
            startday=datetime.datetime.strptime(startdayy,'%Y-%m-%d').date()
            end_date=startday+datetime.timedelta(days=night)

            start_day=jdatetime.datetime.fromgregorian(day=startday.day,month=startday.month,year=startday.year)
            end_date=jdatetime.datetime.fromgregorian(day=end_date.day,month=end_date.month,year=end_date.year)

            #+=====



            #======== search Source and Destination
            try:
                first_link = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="online-tour"]'))
                )
                first_link.click()
                # driver.find_element(By.XPATH,'//*[@id="online-tour"]').click()

                first_link = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="input-group"]//input'))
                )
                first_link.click()
                # driver.find_element(By.XPATH,'//div[@class="input-group"]//input').click()

                while(True):
                    try:
                        driver.find_element(By.XPATH, '//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/input').clear()
                        driver.find_element(By.XPATH, '//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/input').send_keys('مشهد')
                        driver.find_element(By.XPATH,'//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/ul/li[1]/a').find_element(By.XPATH,'//*[text()="خراسان رضوی"]').click()



                        time.sleep(1)
                        driver.find_element(By.XPATH,'//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[3]/div[1]/input').send_keys('کیش')
                        time.sleep(3)
                        first_link = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/ul'))
                        )
                        # first_link.click()
                        driver.find_element(By.XPATH,'//*[@id="online-tour"]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/ul').find_element(By.XPATH,'.//*[text()="هرمزگان"]/..').click()
                        break
                    except:
                        time.sleep(1)
            except:
                ''


            #=== Search Date ==
            # lst_date1=['05/01','4/24','4/25','05/02']
            # lst_date2=['05/05','4/27','4/28','05/06']

            # jalali_date=jdatetime.datetime.fromgregorian(day=7,month=7,year=2024)
            #jalali_date.month
            current=jdatetime.datetime.now()
            current_month=current.month

            tekrar=5
            # for date1,date2 in zip(lst_date1,lst_date2):
            while(True):
                try:


                    if (start_day.month==current_month):
                        data1_column='0'
                        iter1=0
                    else:
                        data1_column='1'
                        iter1=-1

                    date1_day=str(start_day.day)

                    if (end_date.month==current_month):
                        data2_column='0'
                        iter2=0
                    else:
                        data2_column='1'
                        iter2=-1
                    date2_day =str(end_date.day)

                    try:
                        driver.find_element(By.XPATH, '//div[@class="full-width date local"]').click()
                    except:
                        try:
                            driver.find_element(By.XPATH, '//*[@id="fixResearch"]/div/div/div[2]/div/div/button').click()
                            driver.find_element(By.XPATH, '//div[@class="full-width date local"]').click()
                        except:
                            print(f'windows not opened! Tekrar === {tekrar}')
                            tekrar=tekrar-1
                            if (tekrar==0):
                                try:
                                    driver.find_element(By.XPATH, '//*[@id="expireTime"]//button[text()="بروزرسانی جستجو"]').click()
                                except:
                                    ''
                                tekrar=5
                                break


                        ''
                    first_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[text()="برو به امروز"]'))
                    )
                    first_link.click()
                    # driver.find_element(By.XPATH, '//button[text()="برو به امروز"]')


                    driver.find_element(By.XPATH, f'//div[@data-column="{data1_column}"]').find_elements(By.XPATH,f'.//div[contains(@class,"pdp-day") and @value="{date1_day}"]')[iter1].click()
                    # driver.find_element(By.XPATH, f'//div[contains(@class,"pdp-day") and @value="{date1}"]').click()

                    # class="pdp-day"

                    driver.find_element(By.XPATH, f'//div[@data-column="{data2_column}"]').find_elements(By.XPATH,f'//div[contains(@class,"pdp-day") and @value="{date2_day}"]')[iter2].click()
                    # driver.find_element(By.XPATH,f'//div[contains(@class,"pdp-day") and @value="{date2}"]').click()



                    driver.find_element(By.XPATH,f'//*[@id="online-tour"]/div/div[2]/div[4]/button').click()

                    first_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="tour-hotel-result"]/div/div[2]/div[2]/div/div[2]/button'))
                    )
                    # first_link.click()
                    time.sleep(5)


                    #=====
                    #== Test
                    #+====
                    pageSource=driver.page_source

                    parser=etree.HTMLParser()
                    htmlparse=etree.parse(StringIO(pageSource),parser=parser)
                    lst_hotels=htmlparse.xpath('//div[@id="tour-hotel-result"]')

                    result = []
                    for htl in lst_hotels:
                        hotelName = htl.xpath('div/div[2]/div[1]/div/div/div[1]/span[1]')[0].text
                        roomName = htl.xpath('div/div[1]/div[3]/div/div[1]/div[2]/span/text()')[0]

                        hotelPrice = htl.xpath('div/div[2]/div[2]/div/div[1]/span[2]/text()')[0]
                        price_overall = int(hotelPrice.replace('ریال', '').replace(',', '').strip().split('.')[0])
                        price_person = round(price_overall / adults, 2)

                        Go_FLight_brand = htl.xpath('div/div[1]/div[3]/div/div[2]/div[1]/div[1]/div/img')[0].get('src')
                        Go_FLight_brand = Go_FLight_brand.split('/')[-1].split('.')[0]

                        Go_FLight_departure = \
                            htl.xpath('div/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/span[1]/text()')[0]
                        Go_FLight_arrive = htl.xpath('div/div[1]/div[3]/div/div[2]/div[1]/div[4]/span/text()')[0]

                        Return_FLight_brand = htl.xpath('div/div[1]/div[3]/div/div[2]/div[2]/div[1]/div/img')[0].get(
                            'src')
                        Return_FLight_brand = Return_FLight_brand.split('/')[-1].split('.')[0]

                        Return_FLight_departure = \
                            htl.xpath('div/div[1]/div[3]/div/div[2]/div[2]/div[2]/div[1]/span[1]/text()')[0]
                        Return_FLight_arrive = htl.xpath('div/div[1]/div[3]/div/div[2]/div[2]/div[4]/span/text()')[0]

                        # =====
                        go_flight = {
                            "airline": convert_airlines(Go_FLight_brand),
                            # "airline": '',
                            "arrive_time": Go_FLight_departure,
                            # "price": min([flight['fee'] for flight in air['classes']])
                            "price": ""
                        }
                        return_flight = {
                            "airline": convert_airlines(Return_FLight_brand),
                            # "airline": '',
                            "arrive_time": Return_FLight_departure,
                            # "price": min([flight['fee'] for flight in air['classes']])
                            "price": ""
                        }

                        # ---
                        # ===
                        hotel = {}

                        # appended_data = {
                        hotel['hotel_name'] = hotelName
                        hotel['room_name'] = roomName

                        hotel['hotel_star'] = ''

                        hotel['go_flight'] = go_flight
                        hotel['return_flight'] = return_flight

                        # price = round(hotel['room_price'] / self.adults, 2) + hotel['go_flight']['price'] + \
                        #         hotel['return_flight'][
                        #             'price']
                        hotel["commission"] = 0
                        hotel["status"] = "تایید شده"
                        hotel['per_person'] = price_person
                        hotel['total_price'] = convert_to_tooman(hotel['per_person'] * adults)
                        # hotel['total_price'] = ''
                        hotel["system_provider"] = "alwin"
                        hotel["redirect_link"] = "https://allwin24.ir/"
                        result.append(hotel)
                        # ---
                        # print(hotelName)
                    # ========

                    try:
                        driver.find_element(By.XPATH, '//div[@class="full-width date local"]').click()
                    except:
                        driver.find_element(By.XPATH, '//*[@id="fixResearch"]/div/div/div[2]/div/div/button').click()
                        driver.find_element(By.XPATH, '//div[@class="full-width date local"]').click()

                    # driver.quit()
                    # return {'status': True, "data": result, 'message': ""}

                    #== add cache ==
                    try:
                        start_date_geo=str(start_day.togregorian().date())
                        night2=str(night)
                        adults2=str(adults)


                        redis_key = f"ready_{start_date_geo}_{night2}_{adults2}_ALLWIN"
                        add_cache(key=redis_key, data={'data': result})
                        print('Successfuly cache')
                    except Exception as e:
                        print(str(e))
                        print('Failed cache')

                    #===
                    return result,driver


                except:
                    ''


        except:  #
            driver.quit()

            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get("https://www.allwin24.ir")
            time.sleep(3)


            # return {"status": False, "data": [], "message": "اتمام زمان"}

    #


startday=datetime.datetime.now().date()
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.allwin24.ir")
time.sleep(3)
adults=2
lst_dates=[str(startday+datetime.timedelta(days=i)).split(' ')[0] for i in range(1,14)]

while(True):
    time1=datetime.datetime.now()
    #=== 3 night ====
    night=3
    for start_day in lst_dates:
        try:
            res,driver=crawl_Allwin24_withSelenium(driver,start_day,night,adults)
        except:
            ''
        print('dasd')

    #=== 4 night ====
    night=4
    for start_day in lst_dates:
        try:
            res,driver=crawl_Allwin24_withSelenium(driver,start_day,night,adults)
        except:
            ''
        print('dasd')

    time2 = datetime.datetime.now()

    deltaTime=((time2-time1).seconds/60)
    waitTime=int(15-deltaTime)
    print(f'wait time ==== {waitTime}')
    # if (waitTime>0):
    #     time.sleep(waitTime)
