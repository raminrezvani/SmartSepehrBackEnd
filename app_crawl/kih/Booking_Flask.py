import requests
import json
import os
import time

from threading import Thread

# Function to delete cookies.json every 3 hours
def delete_cookies_periodically():
    while True:
        # Wait for 3 hours (3 hours * 60 minutes * 60 seconds)
        time.sleep(3 * 60 * 60)
        # Check if cookies.json exists and delete it
        if os.path.exists('cookies.json'):
            os.remove('cookies.json')
            print("Deleted cookies.json")

# Start the background thread for cookie deletion
cookie_deletion_thread = Thread(target=delete_cookies_periodically)
cookie_deletion_thread.daemon = True  # Daemonize thread to exit when the main program exits
cookie_deletion_thread.start()



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


def get_authorization():
    print(f'-----Booking Authotization -----')
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'analytics_campaign={%22source%22:%22google%22%2C%22medium%22:%22organic%22}; analytics_token=22ffd8a1-e581-be11-efe1-43157fd04a08; SERVERID=fanavaweb3; _yngt_iframe=1; _yngt=4ada5a09-9baf9-95841-17f60-061524e7f4766; __RequestVerificationToken=eL5-NSSEy-Y7wsshrCV-Nsuii8fFBwElkwFha527YS7ZtleRU0K-NGgBh3-qw2scrJWcAKwZBlZTiN0g6GLWWF1Gqqa0wTkwkVmxWcvt3t41; analytics_session_token=76f4fa94-1961-f7df-3e1c-27997364cf77; yektanet_session_last_activity=8/9/2024; _gid=GA1.2.703081956.1723190029; Authentication=13jVmKckM0NT0eI3jcq3mTIwaVU_Hb87ZV3LNPOvGBtV8c5vHn4SlqlbpmolUCHfYQ99n4NzDZX88J22cCeXFSLX3HWRi1LqBwZ8WMjpzYT5CWUXxVHsQ5fGpVecaPH2c8ONr4kFeqBZLSscscr8h6RlAxG8qvlf3EoXEYW0CSqdldlYl7ti43LQbcQwPBsTwQF7Ehd5hQGzGNbCMVjOXRxsMj0Z5kdhijdW0BsM9iBL8Esfe7tCgobeNoLi7O_SlE-iCkZXJfcKAGM72f2YKK9b-lANv7CdhmQWbBq3eF4KPvI4c-he9kyfI9nEewEqioXKQ-kKJBFRJFGfmppH1_aLMowINAVfP0upf8RkbkkbYn7E6XzEPdkmmFxmfy052poag5-48lBb0rsI18P0tQUT9a-GinT1OtvG1jcVhZvK-IIlyZLzFxP9Ecv5bGwp0eEPExYtoxRyn7xHh28MM4908cbVmc9D3dZW7JufQ0L6E8Unjo6hZxc_2rnpqKX8YPYnrckJ1__v2TK2hJCBjBDqYUjxDJAttkbZlmmq39lTJMxXqiI-MYtsnb0hXqI0huKBgdGr_fuF0vc2TgBFq2gwdd8xFT2OfZVM68W_PORW7yNNPeMscrpbSI49RLMvNWmzTKNsIQx8UlXwBUKCxTUPXwnxk06aLqpBGdRq5em3jIfwb4n9kRcE2Jghl1I-wx68EOV5-oGeVG7VLGETf8fX9nNp1qBSclYx1ZppeCrR2wWR92_qpVe6T4JbzmMwrYdmWKoDGvsXZhqC3asRs2vu2veWZFP8IOlxR6BeTrxcmTVq2B65Z3rwliFGTBrMGBawyMuhoYA_eBNlO0dZuC-0XNKg-HHMTTdDXmQc2bpVfhiP31gTOau2e6KLkm3Zf1Y_uJgKKgCmJU1HDL92VuIUkUmz9pHuCv6eMNiJW2v0gLD_NaRS0NHP6CuwOJxgzYetcgIbZaQTg0v-lfkbmA; _dc_gtm_UA-174237991-1=1; _ga=GA1.2.191314830.1719310326; _ga_N9ZBHQ0R9X=GS1.1.1723189964.3.1.1723190107.45.0.0',
        'origin': 'https://www.booking.ir',
        'priority': 'u=1, i',
        'referer': 'https://www.booking.ir/sign-in/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'mobile': '09153148721',
        'password': '@MST8451030yf',
        'countryCode': 'IR',
    }

    req = requests.post('https://www.booking.ir/fa/v2/signinbymobile/', headers=headers, data=data)

    cookies = [f"{key}={value}" for key, value in req.cookies.get_dict().items()]

    headers['Cookie'] = '; '.join(cookies)

    req = requests.get( "https://www.booking.ir/account/getcompanies/", headers=headers)

    data = json.loads(req.text)

    company_id = data['model'][0]['id']

    data = F"id={company_id}"

    req = requests.post("https://www.booking.ir/account/signinbycompany/", headers=headers, data=data)

    return req.cookies


# get_authorization()
#================================

def parse_results(json_res1):
    result=[]
    hotelItineraries=json_res1['model']['hotelBookingSearchResult']['hotelBookingItineraries']

    for hotelItinerary in hotelItineraries:
        hotel_name=hotelItinerary['hotel']['title']
        hotel_stars=hotelItinerary['hotel']['rating']
        total_price=hotelItinerary['bestPackage']['totalPrice']
        # total_price=hotelItinerary['bestPackage']['listPrice']
        room_name=hotelItinerary['bestPackage']['packages'][0]['rooms'][0]['roomTypeTitle'].strip()

        go_flight = {
            "price": None,
            "departure_time": None
        }
        return_flight = {
            "price": None,
            "departure_time": None
        }
        go_flight['airline'] = hotelItinerary['flightItineraries'][0]['flights'][0]['flightsSegments'][0]['operatingAirlineTitle']
        go_flight['arrive_time'] = hotelItinerary['flightItineraries'][0]['flights'][0]['departureDateTime']

        return_flight['airline'] = hotelItinerary['flightItineraries'][1]['flights'][0]['flightsSegments'][0]['operatingAirlineTitle']
        return_flight['arrive_time'] = hotelItinerary['flightItineraries'][1]['flights'][0]['departureDateTime']

        result.append({
            "hotel_name": hotel_name,
            "hotel_star": hotel_stars,
            "hotel_price": ready_price(str(total_price)),
            "total_price": ready_price(str(total_price)),
            "room_name": room_name,
            "go_flight": go_flight,
            "return_flight": return_flight,
            "system_provider": "booking"
        })


    print('finish')

    return result


from datetime import datetime,timedelta



def get_booking_tours(start_date, night_count):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
        end_date = (start_date + timedelta(days=night_count)).strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
        url = f"https://www.booking.ir/trip/?i={start_date}&o={end_date}&r=1&n=&d=1640809&or=1640810&a=2&c=0#/"

        # Load or renew cookies
        cookies_dict = load_cookies()

        while True:
            cookies_string = '; '.join([f'{name}={value}' for name, value in cookies_dict.items()])
            headers = {'Cookie': cookies_string}
            req = requests.get(url, headers=headers)

            if req.status_code != 200:
                print(f'Booking Error --- Status_Code: {req.status_code}')
                cookies_dict = renew_and_save_cookies()  # Renew cookies
            else:
                break

        sessionID = extract_session_id(req.text)
        res1 = requests.get(f'https://www.booking.ir/v2/trip/searchpackage/?sessionid={sessionID}', headers=headers)
        json_res1 = res1.json()
        price = json_res1['model']['hotelBookingSearchResult']['hotelBookingItineraries'][2]['bestPackage']['totalPrice']

        print('Finished')
        # results=parse_results(json_res1)
        return json_res1

    except Exception as e:
        print(f'An error occurred: {e}')

def load_cookies():
    if os.path.exists('cookies.json'):
        with open('cookies.json', 'r') as json_file:
            return json.load(json_file)
    else:
        return renew_and_save_cookies()

def renew_and_save_cookies():
    cookies = get_authorization()
    cookies_dict = {cookie.name: cookie.value for cookie in cookies}
    with open('cookies.json', 'w') as json_file:
        json.dump(cookies_dict, json_file)
    return cookies_dict

def extract_session_id(response_text):
    return response_text.split('sessionId')[1].split(',"basic"')[0].replace(':', '').replace('"', '')


#===== CALLING ==============

from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import json

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=1)

@app.route('/booking_tours', methods=['GET'])
def booking_tours():
    start_date = request.args.get('start_date')
    night_count = request.args.get('night_count', type=int)

    if not start_date or not night_count:
        return jsonify({"error": "Missing start_date or night_count"}), 400

    future = executor.submit(get_booking_tours, start_date, night_count)
    result = future.result()
    # Optionally, you can return a response immediately
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)



# result = get_booking_tours("2024-08-15", 3)

