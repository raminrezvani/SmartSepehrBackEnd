from selenium.webdriver.common.by import By
from app_crawl.helpers import (ready_price, convert_gregorian_date_to_persian, get_env_data, convert_to_tooman, get_driver)


def get_dayan_tours(start_date, night_count):
    # try:
    start_date = convert_gregorian_date_to_persian(start_date, "%Y/%m/%d")['date']

    driver = get_driver()
    # driver = webdriver.Chrome("chromedriver")
    url = f"https://dayansafar.com/api/DeepLink/Hotel/AvailabilityOfToday/V1?cityIataCode=KIH&nights=1&language=fA&utmSource=moghim24"
    driver.get(url)

    # driver.delete_all_cookies()
    # driver.add_cookie(
    #     {'name': 'cookiesession1', 'value': get_env_data("DAYAN_COOKIESESSIN1"), 'domain': get_env_data('DAYAN_DOMAIN')})
    # driver.add_cookie(
    #     {'name': 'XSRF-TOKEN', 'value': get_env_data("DAYAN_XSRF_TOKEN"), 'domain': get_env_data('DAYAN_DOMAIN')})
    # driver.add_cookie(
    #     {'name': 'Sepehr_GUID', 'value': get_env_data("DAYAN_SEPEHR_GUID"), 'domain': get_env_data('DAYAN_DOMAIN')})
    # driver.add_cookie(
    #     {'name': 'B2B_IamToken', 'value': get_env_data("DAYAN_B2B_IAMTOKEN"), 'domain': get_env_data('DAYAN_DOMAIN')})
    # driver.add_cookie(
    #     {'name': 'ASP.NET_SessionId', 'value': get_env_data("DAYAN_ASP_NET_SESSIONID"), 'domain': get_env_data('DAYAN_DOMAIN')})
    # driver.add_cookie(
    #     {'name': 'Language', 'value': get_env_data("DAYAN_LANGUAGE"), 'domain': get_env_data('DAYAN_DOMAIN')})
    # driver.add_cookie({'name': 'To_Destination_Code',
    #                    'value': get_env_data("DAYAN_TO_DESTINATION_CODE"),
    #                    'domain': get_env_data('DAYAN_DOMAIN')})
    # driver.refresh()
    result = []

    # --- redirect button
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

    # --- set date
    while True:
        try:
            departure = driver.find_element(By.CSS_SELECTOR, "[name='txtDepartureDate']")
            if start_date == departure.get_attribute("value"):
                break
            departure.clear()
            departure.send_keys(start_date)
            departure.clear()
            departure.send_keys(start_date)
            departure.clear()
            departure.send_keys(start_date)
            departure.click()
            continue
        except:
            continue

    # --- set night count
    while True:
        try:
            night_count = driver.find_element(By.CSS_SELECTOR,
                                              f"""select[name="dplNights"] option[value="{night_count}"]""")
            night_count.click()
            break
        except:
            continue

    # --- set adults
    while True:
        try:
            adult = driver.find_element(By.CSS_SELECTOR, f"""select[name="dplAdult"] option[value="2"]""")
            adult.click()
            break
        except:
            continue

    # --- set child
    while True:
        try:
            child = driver.find_element(By.CSS_SELECTOR, f"select[name='dplChild'] option[value='0']")
            child.click()
            break
        except:
            continue

    # --- set infant
    while True:
        try:
            infant = driver.find_element(By.CSS_SELECTOR, f"select[name='dplInfant'] option[value='0']")
            infant.click()
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

    # --- check go flight
    go_flight = {}
    try:
        go_flight = driver.find_element(By.CSS_SELECTOR, """.df:has([name="DepartureFlight"]:checked)""")
        go_price = go_flight.find_element(By.CSS_SELECTOR, 'label').text.split('  ')
        go_arrive = go_flight.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
        go_departure_time = go_flight.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
        go_airline = go_flight.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text
        go_flight = {
            "airline": go_airline.split('  ')[-1],
            "arrive_time": go_arrive,
            "departure_time": go_departure_time,
            "price": ready_price(go_price[1])
        }
    except:
        print("--------------------------------")
        print("dayan go flight doesnt exists")
        return result

    # --- check return flight
    return_flight = {}
    try:
        return_flight = driver.find_element(By.CSS_SELECTOR, """.rf:has([name="ReturningFlight"]:checked)""")
        return_price = return_flight.find_element(By.CSS_SELECTOR, 'label').text.split('  ')
        return_arrive = return_flight.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
        return_departure_time = return_flight.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
        return_airline = return_flight.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text
        return_flight = {
            "airline": return_airline.split('  ')[-1],
            "arrive_time": return_arrive,
            "departure_time": return_departure_time,
            "price": ready_price(return_price[1])
        }
    except:
        print("--------------------------------")
        print("dayan return_flight doesnt exists")
        return result

    # --- get hotels
    try:
        hotels = driver.find_elements(By.CSS_SELECTOR, "tr[bgcolor='#EEEEEE']")
        for hotel in hotels:
            hotel_name = hotel.find_element(By.CSS_SELECTOR, 'label').text
            hotel_price_per_person = hotel.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
            hotel_room_name = hotel.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
            hotel_status = hotel.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text
            # ---
            appended_data = {
                "hotel_name": hotel_name,
                "hotel_rooms": hotel_room_name,
                "room_name": hotel_room_name,
                "total_price": convert_to_tooman(int(ready_price(hotel_price_per_person)) * 2),
                "go_flight": go_flight,
                "return_flight": return_flight,
                "status": hotel_status.strip(),
                "system_provider": "dayan",
            }
            result.append(appended_data)
    except:
        print("--------------------------------")
        print("dayan hotels doesnt exists")

    # ---
    driver.close()
    with open('C:\Users\Administrator\Desktop\hotels_providers_api\app_crawl\kih\dayan.html', 'w') as dayan:
        dayan.write(result)
        dayan.close()
    return result
    # except:
    #     return []


# dayan = get_dayan_tours("2022-12-16", 4)
# print("--------------------------------")
# print(dayan)
