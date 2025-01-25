import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, wait,as_completed

from datetime import datetime
import json
import jdatetime

from lxml import etree
from io import StringIO
import requests
from lxml import etree
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests

class Trivago:
    def __init__(self, target, start_date, end_date, adults):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.executor = ThreadPoolExecutor(max_workers=200)

        self.cookies = []

        self.mapping_destination={
            'DXB':'https://www.trivago.com/en-US/lm/hotels-dubai-united-arab-emirates?search=200-15075;dr-',
            'IST':'https://www.trivago.com/en-US/lm/hotels-istanbul-turkey?search=200-15288;dr-'
        }
    def get_result(self):
        try:

            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            start_date=str(start_date).replace('-','')
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            end_date=str(end_date).replace('-','')

            # stay_duration = (end_date - start_date).days

            options = Options()

            # Run Chrome in headless mode
            # options.add_argument("--headless")

            # Further optimizations
            options.add_argument("--no-sandbox")  # Required for certain environments like Docker
            options.add_argument("--disable-dev-shm-usage")  # Disables the /dev/shm memory
            options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
            options.add_argument("--window-size=1920,1080")  # Set a window size to ensure all content is loaded
            options.add_argument("--disable-extensions")  # Disable extensions to speed up performance
            options.add_argument("--disable-infobars")  # Disables the "Chrome is being controlled" banner
            options.add_argument(
                "--disable-blink-features=AutomationControlled")  # Prevents detection as an automated browser

            # Set the path to ChromeDriver (change to your path)
            service = Service("chromedriver.exe")

            # Initialize the WebDriver with the options
            driver = webdriver.Chrome(service=service, options=options)

            # driver=webdriver.Chrome()
            driver.set_page_load_timeout(50)

            driver.maximize_window()
            try:
                driver.get(f'{self.mapping_destination[self.target]}{start_date}-{end_date}-s')
            except:
                ''

            try:
                driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/main/div[1]/div[2]/div/div[3]/div/div[2]/div/div/button/span[2]').click()
            except:
                ''

            #--more deals
            lst_deals=driver.find_elements(By.XPATH,'//button[@data-testid="more-deals"]')

            if (len(lst_deals)==0):
                driver.refresh()


            for deal in lst_deals:
                try:
                    deal.click()
                    driver.switch_to.window(driver.window_handles[0])
                    #-- get deals
                    lst_rooms_items=driver.find_elements(By.XPATH,'//ul[@data-testid="all-slideout-deals"]/li')

                except:
                    ''

            #======
            page_source=driver.page_source

            parser=etree.HTMLParser()
            htmlparsed=etree.parse(StringIO(page_source),parser=parser)

            lst_hotels_items=htmlparsed.xpath('//article')
            lst_hotels=[]
            for hotelItem in lst_hotels_items:

                try:
                    hotelname=hotelItem.xpath('.//button[@data-testid="item-name"]//text()')[0]
                    lst_rooms_items=hotelItem.xpath('..//ul[@data-testid="all-slideout-deals"]/li')
                except:
                    continue
                lst_rooms=[]
                for roomItem in lst_rooms_items:
                    try:
                        provider=roomItem.xpath('.//img[@data-testid="advertiser-logo"]')[0].get('title')
                        price=roomItem.xpath('.//*[@data-testid="recommended-price"]')[0].text
                        roomName=roomItem.xpath('.//div[@class="NiiYax"]/p')[0].text
                        room={}
                        room['name']=roomName
                        room['price']=int(str(price).replace('$',''))*70000
                        room['provider']=provider

                        lst_rooms.append(room)

                        print(f'hotelname ===  {hotelname}  \n  provider === {provider}  \n price == {price}  \n  roomName == {roomName}')
                        # print(f'hotelname ===  {hotelname} ')
                    except:
                        ''

                hotel = {}
                hotel['hotel_name'] = hotelname
                hotel['hotel_star'] = '5'
                hotel['min_price'] = ''
                hotel['provider'] = 'trivago'
                hotel['rooms'] = lst_rooms
                lst_hotels.append(hotel)
            driver.quit()
        except:
            driver.quit()
            lst_hotels=[]

        return lst_hotels




#=============


#
# #=== Alaedin ===
# #
# trivago=Trivago('KIH','2024-10-30','2024-11-04','2')
# trivago.get_result()
# # #===========

    #
    # hotel = {}
    # hotel['hotel_name'] = ''
    # hotel['hotel_star'] = ''
    # hotel['min_price'] = ''
    # hotel['provider'] = ''
    # hotel['rooms'] = [
    #     {
    #         'name': '',
    #         'price': '',
    #         'provider': '',
    #     }
    # ]
    # pass

#
#
# htmlparsed.xpath('//ul[@data-testid="all-slideout-deals"]/li')
#
#
#
# driver.find_element(By.XPATH,'//*[@id="tab-content-DEAL"]/div/div/div/section/ul/li[1]/div[1]/div/div[2]/div[1]/p/span')
# aa=requests.get('https://www.trivago.com/en-US/srl/hotels-paris-france?search=200-22235;dr-20241108-20241112')