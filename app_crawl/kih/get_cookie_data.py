from selenium.webdriver.common.by import By
from app_crawl.helpers import (get_driver, )
from app_crawl.cookie import cookie_data
from urllib.parse import urlparse
from urllib.parse import parse_qs
from requests import request
import json
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import after_response
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

executor = ThreadPoolExecutor(max_workers=30)


class Booking:
    def get_authorization(self):
        url = "https://www.booking.ir/fa/v2/signinbymobile/"

        payload = 'mobile=09153148721&password=@MST8451030yf'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req = request("POST", url, headers=headers, data=payload)

        cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

        headers['Cookie'] = '; '.join(cookies)

        req = request("GET", "https://www.booking.ir/account/getcompanies/", headers=headers, verify=False)

        data = json.loads(req.text)

        company_id = data['model'][0]['id']

        data = F"id={company_id}"

        for _ in range(6):
            req = request("POST", "https://www.booking.ir/account/signinbycompany/", headers=headers, data=data,
                          verify=False)

        return req.cookies

    def set_cookie(self):
        cookies = self.get_authorization()
        # ---
        start_date = datetime.now().strftime('%Y-%m-%d')
        night_count = 3
        # ---
        start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
        end_date = (start_date.date() + timedelta(days=night_count)).strftime("%Y-%m-%d")

        driver = get_driver()

        url = f"https://www.booking.ir/trip/?i={start_date}&o={end_date}&r=1&n=&d=1640809&or=1640810&a=2&c=0#/"
        driver.get(url)
        # ---
        for cookie in cookies:
            driver.add_cookie({'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain})
        driver.refresh()
        # ---
        cookies = [f"{cookie['name']}={cookie['value']};" for cookie in driver.get_cookies()]

        driver.close()
        return ' '.join(cookies)


def get_sepehr_cookie(data):
    try:
        driver = get_driver()
        domain = data['domain']
        url = f"https://{domain}/api/DeepLink/Hotel/AvailabilityOfToday/V1?cityIataCode=KIH&nights=1&language=fA&utmSource=moghim24"
        # https://apk724.tsptick.ir/api/DeepLink/Hotel/AvailabilityOfToday/V1?cityIataCode=KIH&nights=1&language=fA&utmSource=moghim24
        driver.get(url)

        # --- redirect button
        while True:
            try:
                redirect_btn = driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                redirect_btn.click()
                break
            except:
                continue

        if data['domain'] == "sepehrreservation.iranhrc.ir":
            while True:
                try:
                    redirect_btn = driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                    redirect_btn.click()
                    break
                except:
                    continue

            while True:
                try:
                    redirect_btn = driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                    redirect_btn.click()
                    break
                except:
                    continue

        while True:
            try:
                redirect_btn = driver.find_element(By.CSS_SELECTOR, "#Header1_li45 > a")
                redirect_btn.click()
                break
            except:
                continue

        # --- set source
        while True:
            try:
                source = driver.find_element(By.CSS_SELECTOR, "select[name='dplFrom'] option[value='MHD']")
                source.click()
                break
            except:
                continue

        # --- set destination
        while True:
            try:
                destination = driver.find_element(By.CSS_SELECTOR, "select[name='dplTo'] option[value='KIH']")
                destination.click()
                break
            except:
                continue

        # --- click submit
        while True:
            try:
                submit_btn = driver.find_element(By.CSS_SELECTOR, f"[name=btnSubmit]")
                submit_btn.click()
                break
            except:
                continue

        # --- check result
        while True:
            try:
                if len(driver.find_elements(By.CSS_SELECTOR, ".Text02")) == 2:
                    break
                continue
            except:
                continue

        current_url = driver.current_url

        cookies = driver.get_cookies()
        view_state = driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATE')
        view_generator = driver.find_element(By.CSS_SELECTOR, '#__VIEWSTATEGENERATOR')

        data['view_state'] = view_state.get_attribute('value')
        data['view_generator'] = view_generator.get_attribute('value')

        for cookie in cookies:
            cookie_name = cookie['name']
            cookie_value = cookie['value']
            data['cookie'][cookie_name] = cookie_value

        parsed_url = urlparse(current_url)

        data['rnd'] = parse_qs(parsed_url.query)['rnd'][0]

        # ---
        driver.close()
        return True
    except:
        return False


@after_response.enable
def get_all_cookie():
    # ---
    booking = Booking()
    booking = executor.submit(booking.set_cookie)
    # ---
    # dayan_data = cookie_data.DAYAN
    # sepid_data = cookie_data.SEPID_PARVAZ
    # mehrab_data = cookie_data.MEHRAB
    # rahbal_data = cookie_data.RAHBAL
    # tak_setare_data = cookie_data.TAK_SETAREH
    # # hrc_data = cookie_data.HRC
    # # ---
    # executor.submit(get_sepehr_cookie, dayan_data)
    # executor.submit(get_sepehr_cookie, sepid_data)
    # executor.submit(get_sepehr_cookie, mehrab_data)
    # executor.submit(get_sepehr_cookie, rahbal_data)
    # executor.submit(get_sepehr_cookie, tak_setare_data)
    # executor.submit(get_sepehr_cookie, hrc_data)
    # ---
    cookie_data.BOOKING['cookie'] = booking.result()


# get_all_cookie()
