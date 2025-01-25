# #================
# import sys
# sys.path.append(r'C:\Users\Administrator\PycharmProjects\Darukade_Crawler\SepehrSmart\collector_build - Copy\collector_build - Copy\tour-collector-back')
# #=================

import datetime
import time
from urllib.parse import urlparse, parse_qs

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

    def get_driver(self, set_cookie=False):
        domain = self.data.get('domain')
        if set_cookie:
            driver = driver_path()
            driver.get(f"https://{domain}")
            # ---
            for key, value in self.data.get('KIH', {}).get('cookie', {}).items():
                cookie_item = {"name": key, "value": value, 'sameSite': 'Strict'}
                if "name" in cookie_item.keys() and "value" in cookie_item.keys():
                    driver.add_cookie(cookie_item)
            # ---
            driver.get(f"https://{domain}/Systems/FA/Reservation/Flight_NewReservation_Search.aspx")
            self.driver = driver
        else:
            driver = driver_path()
            driver.get(f'https://{domain}')
            self.driver = driver

    def get_validity(self):
        try:
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
            tryIter=5
            while(True):
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
                    self.driver.find_element(By.XPATH,'//*[@id="frmLogin"]/table/tbody/tr[1]/td').click()

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
        submit_btn.click()

    def get_tour_cookie(self, target="KIH"):
        # --- redirect button
        while True:
            try:
                redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                redirect_btn.click()
                break
            except:
                continue

        if self.data['domain'] == "sepehrreservation.iranhrc.ir":
            while True:
                try:
                    redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                    redirect_btn.click()
                    break
                except:
                    continue

            while True:
                try:
                    redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                    redirect_btn.click()
                    break
                except:
                    continue

        while True:
            try:
                redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                redirect_btn.click()
                break
            except:
                continue

        # --- set source
        while True:
            try:
                source = self.driver.find_element(By.CSS_SELECTOR, "select[name='dplFrom'] option[value='MHD']")
                source.click()
                break
            except:
                continue

        # --- set destination
        while True:
            try:
                destination = self.driver.find_element(By.CSS_SELECTOR,
                                                       f"select[name='dplTo'] option[value='{target}']")
                destination.click()
                break
            except:
                continue

        # --- click submit
        while True:
            try:
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, f"[name=btnSubmit]")
                submit_btn.click()
                break
            except:
                continue

        # --- check result
        while True:
            try:
                if len(self.driver.find_elements(By.CSS_SELECTOR, ".Text02")) == 2:
                    break
                continue
            except:
                continue

        current_url = self.driver.current_url

        cookies = self.driver.get_cookies()
        view_state = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATE')
        view_generator = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATEGENERATOR')

        self.data[target]['view_state'] = view_state.get_attribute('value')
        self.data[target]['view_generator'] = view_generator.get_attribute('value')

        self.data[target]['cookie'] = {}

        for cookie in cookies:
            cookie_name = cookie['name']
            cookie_value = cookie['value']
            self.data[target]['cookie'][cookie_name] = cookie_value

        parsed_url = urlparse(current_url)

        self.data[target]['rnd'] = parse_qs(parsed_url.query)['rnd'][0]

        # ---
        return True

    def get_hotel_cookie(self, target="KIH"):
        # --- redirect button
        while True:
            try:
                redirect_btn = self.driver.find_element(By.CSS_SELECTOR, "#Header1_li19 > a")
                redirect_btn.click()
                break
            except:
                continue

        # --- select kih
        while True:
            try:
                destination = self.driver.find_element(By.CSS_SELECTOR, f'#dplTo > option[value="{target}"]')
                destination.click()
                break
            except:
                continue

        # --- search button
        while True:
            try:
                search_btn = self.driver.find_element(By.CSS_SELECTOR, '#btnSearch')
                search_btn.click()
                break
            except:
                continue

        self.data['hotel'] = {}
        # --- hotel viewstate
        view_state = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATE')
        self.data['hotel']['view_state'] = view_state.get_attribute('value')

        # --- event validation
        event_control = self.driver.find_element(By.CSS_SELECTOR, '#__EVENTVALIDATION')
        self.data['hotel']['event_validation'] = event_control.get_attribute('value')

        # --- viewstate generator
        view_state_generator = self.driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATEGENERATOR')
        self.data['hotel']['view_state_generator'] = view_state_generator.get_attribute('value')

        # --- cookie
        # self.data['hotel']['cookie'] = dict()
        cookies = self.driver.get_cookies()
        cookie_result = dict()
        for cookie in cookies:
            cookie_name = cookie['name']
            cookie_value = cookie['value']
            cookie_result[cookie_name] = cookie_value
        self.data['hotel']['cookie'] = cookie_result

    def close_driver(self):
        self.driver.close()
        return True


dayan_cookie = GetSepehrCaptcha(cookie_data.DAYAN)
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
