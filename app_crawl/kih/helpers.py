import jdatetime
from pathlib import Path
import os
import environ
import re
from selenium import webdriver
import redis
import json
from webdriver_manager.chrome import ChromeDriverManager
from django.conf import settings

redis_connection = redis.Redis()


def get_driver(**kwargs):
    """
    get selenium driver
    :return: driver
    """
    base_dir = settings.BASE_DIR
    chrome_path = os.path.join(base_dir, "chromedriver.exe")
    return webdriver.Chrome(chrome_path, **kwargs)


def add_dict_to_redis(key: str, data: [dict, list], expire_time) -> bool:
    """
    add dict or list to redis
    :param key: redis key
    :param data: object or list
    :param expire_time: by seconds
    :return: bool, True => successfully added
    """
    try:
        return redis_connection.set(key, json.dumps(data), ex=expire_time)
    except:
        return False


def get_dict_to_redis(key: str):
    """
    get redis data
    :param key: redis key
    :return: data
    """
    try:
        return json.loads(redis_connection.get(key).decode("utf-8"))
    except:
        return []


def delete_key_from_redis(key: str):
    """
    delete key and data from redis
    :param key: redis key
    :return: None
    """
    try:
        return redis_connection.delete(key)
    except:
        return False


def check_redis_key(key: str):
    """
    check redis has key or not
    :param key: redis key
    :return: True => redis has got the key
    """
    try:
        return str.encode(key) in redis_connection.keys()
    except:
        return False


def get_env_data(key) -> str:
    """
    get data from .env file
    :param key: .env file key
    :return: .env file data
    """
    BASE_DIR = Path(__file__).resolve().parent
    ENV_PATH = os.path.join(BASE_DIR, '.env')

    env = environ.Env(
        DEBUG=(bool, False)
    )

    environ.Env.read_env(os.path.join(ENV_PATH))

    try:
        return env(key)
    except:
        return ""


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


def convert_persian_date_to_gregorian(date: str, template: str = "%Y-%m-%d") -> dict:
    """
    convert jalali date to gregorian
    :param date: format ==> YYYY/MM/DD
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
            "date": jdatetime.date(year=year, month=month, day=day, locale='fa_IR').togregorian().strftime(template)
        }
    except:
        return {"status": False, "message": "something went wrong", "date": None}


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


def ready_sepehr_hotel_name(name: str) -> str:
    """
    remove sepehr hotel name noises
    :param name: hotel name
    :return: hotel name without noise
    """
    name = convert_persian_number_to_english(name)
    name = name.replace("*", "")
    name = ''.join([i for i in name if not i.isdigit()])
    name = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", name)
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.replace('KIH', '')
    name = name.replace('kih', '')
    name = name.replace('GSM', '')
    name = name.replace('gsm', '')
    name = name.replace('گارانتي', '')
    name = name.replace('-', '')
    name = name.replace('_', '')
    name = name.replace('ـ', '')
    name = name.replace('آ', 'ا')
    name = name.replace('ي', 'ی')
    name = name.replace('سوئيت', '')
    name = name.replace('ُ', '')  # ُ
    name = name.replace('هتل', '')
    name = name.replace('کیش', '')
    name = name.replace('قشم', '')
    name = name.replace('درگهان', '')
    return name.strip()


def ready_sepehr_gsm_hotel_name(name: str) -> str:
    """
    remove sepehr gsm hotel name noises
    :param name: hotel name
    :return: hotel name without noise
    """
    name = convert_persian_number_to_english(name)
    name = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", name)
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.replace('قشم', '')
    name = name.replace('درگهان', '')
    name = name.replace('ُ', '')  # ُ
    name = name.replace('ي', 'ی')
    name = name.replace('آ', 'ا')
    name = name.replace('قشم', '')
    name = name.replace('درگهان', '')
    name = name.replace('GSM', '')
    name = name.replace('gsm', '')
    name = name.replace('_', ' ')
    name = name.replace('  ', ' ')
    return name


def convert_to_tooman(price) -> int:
    """
    convert rial price to tooman
    :param price: rial price
    :return: tooman price
    """
    return int(float(price) / 10)


def convert_airlines(airline_code: str) -> str:
    """
    convert airline iata code to persian name
    :param airline_code: airline iata code
    :return: airline persian name
    """
    airlines = {
        "ZV": "زاگرس",
        "B9": "ایران ایر تور",
        "Y9": "کیش ایر",
        "HH": "تابان",
        "IS": "سپهران",
        "I3": "اتا",
        "JI": "معراج",
        "IV": "کاسپین",
        "A7": "آسا جت",
        "EP": "آسمان",
        "AK": "اترک",
        "IR": "ایران ایر",
        "PA": "پارس ایر",
        "Z4": "پویا",
        "TF": "تفتان",
        "RI": "چابهار",
        "Z3": "ساها",
        "QB": "قشم ایر",
        "W5": "ماهان",
        "VR": "وارش",
        "NV": "کارون",
        "6A": "آرمنیا ایرویز",
        "AZ": "آلیتالیا",
        "EY": "اتحاد",
        "OS": "اتریشی",
        "KK": "اطلس گلوبال",
        "EK": "امارات",
        "PS": "اکراین",
        "AF": "ایرفرانس",
        "A3": "ایژین",
        "BA": "بریتیش ایرویز",
        "PC": "پگاسوس",
        "TK": "ترکیش",
        "CZ": "چاینا",
        "XQ": "سان اکسپرس",
        "WY": "عمان ایر",
        "QR": "قطر",
        "GF": "گلف ایر",
        "LH": "لوفنت هانزا",
        "N4": "نوردویند",
        "XC": "کرندون",
        "V0": "کونویاسا",
        "KU": "کویت",
        "KL": "کی ال ام"
    }
    airline_code = airline_code.replace('_', '')
    return airlines.get(airline_code, airline_code)
