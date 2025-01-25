import json
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from app_crawl.helpers import (ready_price, get_driver)
from time import sleep
from requests import request


def get_authorization():
    url = "https://www.booking.ir/fa/v2/signinbymobile/"

    payload = 'mobile=09153148721&password=@MST8451030yf'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    req = request("POST", url, headers=headers, data=payload)

    cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

    headers['Cookie'] = '; '.join(cookies)

    req = request("GET", "https://www.booking.ir/account/getcompanies/", headers=headers)

    data = json.loads(req.text)

    company_id = data['model'][0]['id']

    data = F"id={company_id}"

    req = request("POST", "https://www.booking.ir/account/signinbycompany/", headers=headers, data=data)

    return req.cookies


def get_booking_tours(start_date, night_count):
    try:
        cookies = get_authorization()
        start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
        end_date = (start_date.date() + timedelta(days=night_count)).strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
        driver = get_driver()
        # driver = webdriver.Chrome("chromedriver")
        url = f"https://www.booking.ir/trip/?i={start_date}&o={end_date}&r=1&n=&d=1640809&or=1640810&a=2&c=0#/"
        driver.get(url)
        # ---
        for cookie in cookies:
            driver.add_cookie({'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain})
        driver.refresh()
        # ---
        while True:
            try:
                print("--------------------------------")
                driver.find_element(By.CSS_SELECTOR, ".loading__wrapper")
                print("booking loading page")
                sleep(.5)
                continue
            except:
                break
        # ---
        result = []
        tours = driver.find_elements(By.CSS_SELECTOR, ".hotels-list__hotel")
        for tour in tours:
            hotel_name = tour.find_element(By.CSS_SELECTOR, '.hotels-list__hotel-title span').text
            hotel_stars = 5 - len(tour.find_elements(By.CSS_SELECTOR, '.hotels-list__hotel-title .icon-star--disabled'))
            hotel_price = tour.find_element(By.CSS_SELECTOR, '.hotels-list__price:not(.hotels-list__price--before-discount) span').text
            flights = tour.find_elements(By.CSS_SELECTOR, '.flights-list__box.flights-list__box--internal')
            go_flight = {
                "price": None,
                "departure_time": None
            }
            return_flight = {
                "price": None,
                "departure_time": None
            }
            for index, flight in enumerate(flights):
                title = flight.find_element(By.CSS_SELECTOR, '.flight-route__title').text
                time = flight.find_element(By.CSS_SELECTOR,
                                           '.flight-route__start-point.flight-route__start-point--hotel-list span:first-of-type').text
                if index == 0:
                    go_flight['airline'] = title
                    go_flight['arrive_time'] = time
                else:
                    return_flight['airline'] = title
                    return_flight['arrive_time'] = time
            # ---
            result.append({
                "hotel_name": hotel_name,
                "hotel_star": hotel_stars,
                "hotel_price": ready_price(hotel_price),
                "total_price": ready_price(hotel_price),
                "room_name": "دو تخته",
                "go_flight": go_flight,
                "return_flight": return_flight,
                "system_provider": "booking"
            })
        # ---
        driver.close()
        return result
    except:
        return []


# result = get_booking_tours("2022-12-20", 4)
# print("--------------------------------")
# print(result)

# print("--------------------------------")
# print(get_authorization())
