# #================
# import sys
# sys.path.append(r'C:\Users\Administrator\PycharmProjects\Darukade_Crawler\SepehrSmart\collector_build - Copy\collector_build - Copy\tour-collector-back')
# #=================

import datetime
import time
from urllib.parse import urlparse, parse_qs
import redis
import json

from selenium.webdriver.common.by import By

from app_company.models import Company, CompanyAccountSign, Provider
from app_crawl.helpers import (get_driver as driver_path, )
from app_crawl.cookie import cookie_data
from requests import request
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GetSepehrCaptcha:

    def __init__(self, data):
        self.data = data
        self.driver = None
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    def get_driver(self, set_cookie=False):
        domain = self.data.get('domain')
        if set_cookie:
            self.driver = driver_path()
            # ===
            self.driver.set_page_load_timeout(5)  # Time in seconds
            # ====
            try:
                self.driver.get(f"https://{domain}")
            except:
                self.driver.execute_script("window.stop();")

            # ---
            for key, value in self.data.get('KIH', {}).get('cookie', {}).items():
                cookie_item = {"name": key, "value": value, 'sameSite': 'Strict'}
                if "name" in cookie_item.keys() and "value" in cookie_item.keys():
                    self.driver.add_cookie(cookie_item)
            # ---
            try:
                self.driver.get(f"https://{domain}/Systems/FA/Reservation/Flight_NewReservation_Search.aspx")
            except:
                self.driver.execute_script("window.stop();")

            self.driver = self.driver
        else:
            self.driver = driver_path()
            # ===
            self.driver.set_page_load_timeout(5)  # Time in seconds
            # ====
            try:
                self.driver.get(f'https://{domain}')
            except:
                self.driver.execute_script("window.stop();")
            self.driver = self.driver

    def get_validity(self,provider_code):
        try:

            #---- read from redis ---
            try:
                self.data=json.loads(self.redis_client.get(provider_code))
            except:
                print(f'providerCode  {provider_code} __ not in Redis')
            #------------



            kih_cookie = self.data.get("KIH", {})
            cookies = kih_cookie.get("cookie", {})

            now_date = datetime.datetime.now()
            rnd = 500

            headers = {
                'authority': self.data['domain'],
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': f'https://{self.data["domain"]}',
                'referer': f"https://{self.data['domain']}/Systems/FA/Reservation/Tour_NewReservation_Search2.aspx?action=display&rnd={rnd}",
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'x-microsoftajax': 'Delta=true',
                'x-requested-with': 'XMLHttpRequest',
            }

            params = {
                'action': 'display',
                'rnd': rnd,
            }

            data = {
                'ScriptManager1': 'UpdatePanel1|btnSubmit',
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': kih_cookie.get('view_state'),
                '__VIEWSTATEGENERATOR': kih_cookie.get('view_generator'),
                'dplFrom': '',
                'dplTo': "",
                'dplHotelName': '0',
                'txtDepartureDate': "",
                'dplNights': f"",
                'dplAdult': '2',
                'dplChild': '0',
                'dplInfant': '0',
                # 'DepartureFlight': 'rptFlights_NonBackToBack$ctl02$rptFlight_Seats$ctl01$rdoFlight',
                # 'ReturningFlight': 'rptFlights_NonBackToBack$ctl04$rptFlight_Seats$ctl01$rdoFlight',
                '__ASYNCPOST': 'true',
                'btnSubmit': 'جستجو',
            }

            request(
                "POST",
                f"https://{self.data['domain']}/Systems/FA/Reservation/Tour_NewReservation_Search2.aspx",
                params=params,
                cookies=cookies,
                headers=headers,
                data=data,
                verify=False
            )

            res = request(
                "GET",
                f"https://{self.data['domain']}/Systems/FA/Reservation/Tour_NewReservation_Search2.aspx?action=display&rnd={rnd}",
                cookies=cookies,
                verify=False
            )

            if "متاسفانه در اجرای دستورات خطایی رخ داده است" in res.text:
                return True
            else:
                return False
        except:
            return False
        # ---

    def get_captcha_image(self):
        try:
            self.driver.close()
        except:
            pass
        self.get_driver()
        image = self.driver.find_element(By.CSS_SELECTOR, '#imgCaptcha')
        return image.get_attribute("src")

    def login_sepehr(self, recaptcha_value, provider_code, company: Company):

        if (self.driver is None):
            print('error Driver None')

        try:
            qs_provider = Provider.objects.filter(soft_delete=False, code=provider_code)
            if not qs_provider:
                return None
            provider = qs_provider.last()
            # ---
            qs_sign = CompanyAccountSign.objects.filter(soft_delete=False, company=company, provider=provider)
        except:
            qs_sign = None
        # ---
        # if qs_sign:
        # else:
        #     agency = self.driver.find_element(By.CSS_SELECTOR, '#dplLoginMode > option:nth-child(1)')
        # ---
        if qs_sign:
            tryIter = 5
            while (True):
                try:
                    agency = self.driver.find_element(By.CSS_SELECTOR, '#dplLoginMode > option:nth-child(2)')
                    agency.click()
                    sign = qs_sign.last()
                    username_val = sign.username
                    password_val = sign.password
                    username = self.driver.find_element(By.CSS_SELECTOR, '#txtUsername')
                    username.clear()
                    username.send_keys(username_val)
                    # ---
                    password = self.driver.find_element(By.CSS_SELECTOR, '#txtPassword')
                    password.clear()
                    password.send_keys(password_val)
                    break
                except:
                    self.driver.find_element(By.XPATH, '//*[@id="frmLogin"]/table/tbody/tr[1]/td').click()

        # if self.data.get('domain') == "sepehrreservation.iranhrc.ir":
        #     username_val = "mojalal safar"
        #     password_val = "MST1231020"
        # elif self.data.get('domain') == "www.opo24.ir":
        #     username_val = "MOJALAL"
        #     password_val = "123456789"
        # elif self.data.get('domain') == "www.parmistkt.ir":
        #     username_val = "mojalal"
        #     password_val = "mst123456"
        # elif self.data.get('domain') == "www.hamsafargasht24.ir":
        #     username_val = "mojalal"
        #     password_val = "123456789"
        # elif self.data.get('domain') == "fk24.ir":
        #     username_val = "MOJALALSAFARMHD"
        #     password_val = "mst1231020"
        # elif self.data.get('domain') == "www.shayangasht.ir":
        #     username_val = "MOJALAL"
        #     password_val = "MST1231020"
        # else:
        #     username_val = "mojalal"
        #     password_val = "mst1231020"
        # ---
        recaptcha_field = self.driver.find_element(By.CSS_SELECTOR, '#txtCaptchaNumber')
        recaptcha_field.clear()
        recaptcha_field.send_keys(recaptcha_value)
        # ---
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, '#btnLogin')
        try:
            submit_btn.click()
        except:
            self.driver.execute_script("window.stop();")

    def try_another_source(self,NewSOURCE):
        # --- set source
        while True:
            try:
                lst_mabda = self.driver.find_element(By.XPATH, "//select[@name='dplFrom']").find_elements(By.XPATH,
                                                                                                          './/option')
                lst_mabda = [a.get_attribute('value') for a in lst_mabda]
                if (NewSOURCE not in lst_mabda):
                    return False

                source = self.driver.find_element(By.CSS_SELECTOR,
                                                  f"select[name='dplFrom'] option[value='{NewSOURCE}']")
                source.click()
                time.sleep(3)
                break
            except:
                print('New Source loop_5')
                continue
        return


    def insertCookie_intoDB(self,provider):


        self.redis_client.set(provider,json.dumps(self.data))
        # Verify the data was inserted
        retrieved_value = self.redis_client.get(provider)
        if retrieved_value:
            print(f"Cookie _ {provider} Insert into DBRetrieved:")
        #===========

        return True

    def GetCookie_FromDB(self,provider):


        if (self.redis_client.exists(provider)):
            res=self.redis_client.get(provider)
            self.data=json.loads(res)
            return True

        return False



    def get_tour_cookie(self, target="KIH",SourceMabda="MHD"):

        # --- redirect button
        while True:
            try:
                redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                redirect_btn.click()
                break
            except:
                try:
                    if ('Tour_NewReservation' in self.driver.current_url):
                        break

                    redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_HeaderPublic1_li45 > a")
                    redirect_btn.click()
                    break
                except:
                    try:
                        self.driver.refresh()
                    except:
                        self.driver.execute_script("window.stop();")

                    print('loop_1')
                    continue
        print('pass_1')

        # if self.data['domain'] == "sepehrreservation.iranhrc.ir":
        #     while True:
        #         try:
        #             redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
        #             redirect_btn.click()
        #             break
        #         except:
        #             print('loop_2')
        #             continue
        #
        #     while True:
        #         try:
        #             redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
        #             redirect_btn.click()
        #             break
        #         except:
        #             print('loop_3')
        #             continue

        while True:
            try:
                redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                redirect_btn.click()
                break
            except:
                if ('Tour_NewReservation' in self.driver.current_url):
                    break

                try:
                    redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_HeaderPublic1_li45 > a")
                    redirect_btn.click()
                    break
                except:
                    print('loop_4')
                    continue
        print('pass_2')
        # --- set source
        while True:
            try:
                lst_mabda = self.driver.find_element(By.XPATH, "//select[@name='dplFrom']").find_elements(By.XPATH,'.//option')
                lst_mabda=[a.get_attribute('value') for a in lst_mabda]
                if (SourceMabda not in lst_mabda):
                    return False

                source = self.driver.find_element(By.CSS_SELECTOR, f"select[name='dplFrom'] option[value='{SourceMabda}']")
                source.click()
                break
            except:
                print('loop_5')
                continue
        print('pass_3')
        # --- set destination
        time.sleep(2)
        amount_try=5
        source_try=["MHD","THR","SYZ"]

        while True:
            try:
                successful=0
                for SourceMabdaNew in source_try:
                    self.driver.execute_script("window.stop();")

                    #=========== check for a source (is there target??) ===
                    lst_des = self.driver.find_elements(By.XPATH, "//select[@name='dplTo']/option")
                    lst_des=[a.get_attribute('value') for a in lst_des]
                    if (target not in lst_des ):
                        self.try_another_source(NewSOURCE=SourceMabdaNew)
                        continue
                    destination = self.driver.find_element(By.CSS_SELECTOR,
                                                           f"select[name='dplTo'] option[value='{target}']")
                    destination.click()
                    successful=1
                    break
                if (successful==1):
                    break
                else:
                    return False
            except:
                if (amount_try<=0):
                    print(f'has not KIH!!!')
                    return False

                print('loop_6')
                amount_try=amount_try-1
                continue

                #
                # try:
                #     # select first one (if not exists)
                #     destination=self.driver.find_element(By.XPATH,'//*[@id="dplTo"]/option[1]')
                #     destination.click()
                #     break
                # except:
                #     print('loop_6')
                #     continue


        print('pass_4')

        # --- click submit
        while True:
            try:
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, f"[name=btnSubmit]")
                submit_btn.click()
                break
            except:
                print('loop_7')
                continue

        print('pass_5')
        # # --- check result
        # while True:
        #     try:
        #         if len(self.driver.find_elements(By.CSS_SELECTOR, ".Text02")) == 2:
        #             break
        #         continue
        #     except:
        #         print('loop_8')
        #         continue

        while (True):
            try:
                current_url = self.driver.current_url
                cookies = self.driver.get_cookies()
                break
            except:
                print('loop_cookie')
                self.driver.execute_script("window.stop();")
                continue
        print('pass_6')

        while(True):
            try:
                view_state = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATE')
                view_generator = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATEGENERATOR')
                self.data[target]['view_state'] = view_state.get_attribute('value')
                self.data[target]['view_generator'] = view_generator.get_attribute('value')
                print('pass_7')
                break
            except:
                print('loop_view_state')
                self.driver.execute_script("window.stop();")
                continue


        self.data[target]['cookie'] = {}
        print('pass_8')
        for cookie in cookies:
            cookie_name = cookie['name']
            cookie_value = cookie['value']
            self.data[target]['cookie'][cookie_name] = cookie_value
        print('pass_9')
        parsed_url = urlparse(current_url)

        self.data[target]['rnd'] = parse_qs(parsed_url.query)['rnd'][0]
        print('pass_10')
        print(' rnd ====' + str(self.data[target]['rnd']))
        # ---





        return True

    def get_hotel_cookie(self, target="KIH",provider=""):
        # --- redirect button
        while True:
            try:
                redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li19 > a")
                redirect_btn.click()
                break
            except:

                if ('Hotel_NewReservation' in self.driver.current_url):
                    break

                try:
                    # redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_HeaderPublic1_li45 > a")
                    redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_HeaderPublic1_li19 > a")
                    redirect_btn.click()
                    break
                except:
                    print('loop_1')
                    continue

        # --- select kih
        time.sleep(2)
        amount_try=5
        while True:
            try:

                destination = self.driver.find_element(By.CSS_SELECTOR, f'#dplTo > option[value="{target}"]')
                destination.click()
                break
            except:

                try:
                    self.driver.refresh()
                except:
                    self.driver.execute_script("window.stop();")

                if (amount_try <= 0):
                    print(f'has not KIH!!!')
                    return False

                amount_try=amount_try-1
                print('loopppp_1')
                continue
                #
                #     # select first one (if not exists)
                #     destination=self.driver.find_element(By.XPATH,'//*[@id="dplTo"]/option[1]')
                #     destination.click()
                #     break
                # except:
                #     print('loopppp_1')
                #     continue

        # --- search button
        while True:
            try:
                search_btn = self.driver.find_element(By.CSS_SELECTOR, '#btnSearch')
                search_btn.click()
                break
            except:
                try:
                    search_btn = self.driver.find_element(By.CSS_SELECTOR, '#btnSubmit')
                    search_btn.click()
                    break
                except:
                    try:
                        search_btn = self.driver.find_element(By.XPATH, '//input[@value="جستجو"]')
                        search_btn.click()
                        break
                    except:
                        try:
                            self.driver.refresh()
                        except:
                            self.driver.execute_script("window.stop();")
                        print('loopppp_2')
                        continue

        self.data['hotel'][target] = {}
        # --- hotel viewstate
        try:
            self.driver.execute_script("window.stop();")
        except:
            ''
        while (True):
            try:
                view_state = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATE')
                self.data['hotel']['view_state'] = view_state.get_attribute('value')
                break
            except:
                self.driver.refresh()
                self.driver.execute_script("window.stop();")
                print('loopppp_3')
                continue

        # --- event validation
        while (True):
            try:
                event_control = self.driver.find_element(By.CSS_SELECTOR, '#__EVENTVALIDATION')
                self.data['hotel']['event_validation'] = event_control.get_attribute('value')
                break
            except:
                self.driver.execute_script("window.stop();")
                print('loopppp_4')
                break  # not havind  __EVENTVALIDATION for rahbal
                # continue

        # --- viewstate generator
        while (True):
            try:
                view_state_generator = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATEGENERATOR')
                self.data['hotel']['view_state_generator'] = view_state_generator.get_attribute('value')
                break

            except:
                self.driver.execute_script("window.stop();")
                print('loopppp_5')
                continue

                # --- cookie
        # self.data['hotel']['cookie'] = dict()

        while (True):
            try:
                cookies = self.driver.get_cookies()
                break
            except:
                print('loop_cookie')
                self.driver.execute_script("window.stop();")
                continue

        cookie_result = dict()
        for cookie in cookies:
            cookie_name = cookie['name']
            cookie_value = cookie['value']
            cookie_result[cookie_name] = cookie_value
        self.data['hotel'][target]['cookie'] = cookie_result

    def close_driver(self):
        self.driver.close()
        return True

eram2mhd_cookie=GetSepehrCaptcha(cookie_data.ERAM2MHD)
touristkish_cookie=GetSepehrCaptcha(cookie_data.TOURISTKISH)
dayan_cookie = GetSepehrCaptcha(cookie_data.DAYAN)
safiran_cookie = GetSepehrCaptcha(cookie_data.SAFIRAN)
hamood_cookie = GetSepehrCaptcha(cookie_data.HAMOOD)
sepid_parvaz_cookie = GetSepehrCaptcha(cookie_data.SEPID_PARVAZ)
mehrab_cookie = GetSepehrCaptcha(cookie_data.MEHRAB)
rahbal_cookie = GetSepehrCaptcha(cookie_data.RAHBAL)
tak_setareh_cookie = GetSepehrCaptcha(cookie_data.TAK_SETAREH)
hrc_cookie = GetSepehrCaptcha(cookie_data.HRC)
omid_oj_cookie = GetSepehrCaptcha(cookie_data.OMID_OJ)
parmis_cookie = GetSepehrCaptcha(cookie_data.PARMIS)
hamsafar_cookie = GetSepehrCaptcha(cookie_data.HAMSAFAR)
iman_cookie = GetSepehrCaptcha(cookie_data.IMAN)
flamingo_cookie = GetSepehrCaptcha(cookie_data.FLAMINGO)
shayan_gasht_cookie = GetSepehrCaptcha(cookie_data.SHAYAN_GASHT)
dolfin_cookie = GetSepehrCaptcha(cookie_data.DOLFIN)
yegane_fard_cookie = GetSepehrCaptcha(cookie_data.YEGANE_FARD)

moeindarbari_cooke=GetSepehrCaptcha(cookie_data.MOEINDARBARI)
darvishi_cooke=GetSepehrCaptcha(cookie_data.DARVISHI)

