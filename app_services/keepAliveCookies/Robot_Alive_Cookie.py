import json
import redis
import time
from requests import request
from concurrent.futures import ThreadPoolExecutor
# from app_crawl.cookie import cookie_data
import cookie_data
import logging
import colorlog

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# Configure colored logging for console and plain logging for file
logger = logging.getLogger(__name__)

# Create handlers for console (colored) and file (plain)
console_handler = colorlog.StreamHandler()
file_handler = logging.FileHandler('captcha_validator.log')

# Define color formatter for console
color_formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',  # Default INFO color (can be overridden for True/False)
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Define plain formatter for file
plain_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Set formatters for handlers
console_handler.setFormatter(color_formatter)
file_handler.setFormatter(plain_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)  # Set logging level to INFO or higher

# Global constants and configurations
REDIS_CLIENT = redis.Redis(host='localhost', port=6379, db=0)
DAYAN_COOKIE = cookie_data.DAYAN
MAX_WORKERS = 10  # Adjust based on your system's capabilities or I/O limits


def check_validation(domain, view_state, view_generator, cookies, is_ready_tour):
    """
    Check the validation of a tour or hotel reservation page by making HTTP requests.
    Returns True if an error occurs (indicating invalidation), False otherwise.
    """
    try:
        rnd = 500
        headers = {
            'authority': domain,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': f'https://{domain}',
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

        params = {'action': 'display', 'rnd': rnd}

        if is_ready_tour:
            data = {
                'ScriptManager1': 'UpdatePanel1|btnSubmit',
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': view_generator,
                'dplFrom': '',
                'dplTo': '',
                'dplHotelName': '0',
                'txtDepartureDate': '',
                'dplNights': '',
                'dplAdult': '2',
                'dplChild': '0',
                'dplInfant': '0',
                '__ASYNCPOST': 'true',
                'btnSubmit': 'جستجو',
            }
            referer_url = f"https://{domain}/Systems/FA/Reservation/Tour_NewReservation_Search2.aspx?action=display&rnd={rnd}"
        else:  # BuildTour (Hotel)
            data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': view_generator,
                'dplTo': '',
                'dplHotelName': '0',
                'txtCheckinDate': '',
                'dplNights': '2',
                'btnSearch': 'جستجو',
            }
            referer_url = f"https://{domain}/Systems/FA/Reservation/Hotel_NewReservation_Search.aspx?action=display&rnd={rnd}"

        # Make POST request
        headers['referer'] = referer_url
        request(
            "POST",
            f"https://{domain}/{referer_url.split('/')[-1]}",
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False
        )

        # Make GET request to check response
        res = request(
            "GET",
            referer_url,
            cookies=cookies,
            verify=False
        )

        status = "متاسفانه در اجرای دستورات خطایی رخ داده است" in res.text
        return status

    except Exception as e:
        logger.error(f"Error in check_validation for domain {domain}: {e}")
        return False


def process_provider(provider):
    """
    Process a single provider by fetching data from Redis and checking validations.
    Logs the status for each validation with colored output.
    """
    if REDIS_CLIENT.exists(provider):
        data = json.loads(REDIS_CLIENT.get(provider))
        domain = data['domain']
        results = {}

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Process hotel keys (BuildTour)
            hotel_tasks = []
            for key in data['hotel'].keys():
                if key not in ['view_state', 'event_validation', 'view_state_generator'] and data['hotel'][key] != {}:
                    cookies = data['hotel'][key].get('cookie', {})
                    hotel_tasks.append(executor.submit(
                        check_validation, domain, data['hotel']['view_state'], data['hotel']['view_state_generator'],
                        cookies, False
                    ))

            # Process tour keys (ReadyTour)
            tour_tasks = []
            for key in data.keys():
                if key not in ['hotel', 'domain'] and data[key] != {}:
                    cookies = data[key].get('cookie', {})
                    tour_tasks.append(executor.submit(
                        check_validation, domain, data[key]['view_state'], data[key]['view_generator'], cookies, True
                    ))

            # Collect and log results for hotels
            for task, key in zip(hotel_tasks, [k for k in data['hotel'].keys() if
                                               k not in ['view_state', 'event_validation', 'view_state_generator'] and
                                               data['hotel'][k] != {}]):
                status = task.result()
                results[f'hotel_{key}'] = status
                if status:
                    logger.info(f"Provider: {provider}, hotel_{key} === True",
                                extra={'log_color': 'cyan'})  # Cyan for True
                else:
                    logger.info(f"Provider: {provider}, hotel_{key} === False",
                                extra={'log_color': 'red'})  # Green for False

            # Collect and log results for tours
            for task, key in zip(tour_tasks,
                                 [k for k in data.keys() if k not in ['hotel', 'domain'] and data[k] != {}]):
                status = task.result()
                results[f'tour_{key}'] = status
                if status:
                    logger.info(f"Provider: {provider}, tour_{key} === True",
                                extra={'log_color': 'cyan'})  # Cyan for True
                else:
                    logger.info(f"Provider: {provider}, tour_{key} === False",
                                extra={'log_color': 'red'})  # Green for False



        return data
    logger.warning(f"Provider {provider} not found in Redis", extra={'log_color': 'yellow'})


def main():
    """
    Main function to process multiple providers concurrently in a loop every 1 hour.
    """
    providers = [
        'safiran', 'darvishi', 'moeindarbari', 'hamood', 'dayan', 'kimiya',
        'eram2mhd', 'sepid_parvaz', 'mehrab', 'rahbal', 'tak_setareh', 'hrc',
        'omid_oj', 'parmis', 'hamsafar', 'iman_amin', 'flamingo', 'shayan_gasht',
        'dolfin', 'yegane_fard'
    ]

    while True:
        logger.info("Starting validation cycle...", extra={'log_color': 'green'})
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            executor.map(process_provider, providers)

        logger.info("Validation cycle completed. Sleeping for 5 minutes...", extra={'log_color': 'green'})
        time.sleep(5*60)  # Sleep for 1 hour (3600 seconds)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Script terminated by user", extra={'log_color': 'green'})
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}", extra={'log_color': 'red'})









