import re
from datetime import datetime
from urllib.parse import urlparse
from uuid import UUID

from rest_framework import status as rest_status


def validate_national_code(national_code: str) -> bool:
    """
    check if national code is valid
    :param national_code: str ==> national_code that you want to check
    :return: bool ==> True = national code is correct
    """
    if not re.search(r'^\d{10}$', national_code):
        return False
    check = int(national_code[9])
    s = sum(int(national_code[x]) * (10 - x) for x in range(9)) % 11
    return check == s if s < 2 else check + s == 11


def validate_url(url: str) -> bool:
    """
    check if url is valid
    :param url: str ==> url that you want to check
    :return: bool ==> True = url is correct
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def validate_email(email: str) -> bool:
    """
    check if email address is valid
    :param email: str ==> email that you want to check
    :return: bool ==> True = email is correct
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def validate_password(password: str) -> bool:
    """
    check if password is valid
    :param password: password that you want to check
    :return: bool ==> True = password is correct
    """
    try:
        return len(password) > 7
    except:
        return False


def validate_token(token: [str, int]) -> bool:
    """
    check if token is valid
    :param token: token that you want to check
    :return: bool ==> True = token is correct
    """
    return str(token).isnumeric() and len(token) == 5


def validate_text(text, length=1) -> bool:
    """
    check if text is valid or not
    :param text: text that you want to check
    :param length: text minimum length
    :return: bool ==>  True = text is correct
    """
    try:
        return len(text) > length
    except:
        return False


def validate_uid(u_id) -> bool:
    """
    check if u_id is valid or not
    :param u_id: u_id that you want to check
    :return: bool ==> True = u_id is correct
    """
    return len(u_id) > 5 and u_id.startswith("J") and u_id.endswith("J")


def validate_phone(phone_number: str, region="IR") -> bool:
    """
    check if phone number is valid
    :param phone_number: str ==> phone number that you want check
    :return: bool ==> True = phone is correct
    """
    return len(phone_number) == 11 and str(phone_number).isnumeric()
    # try:
    #     parse_number = phonenumbers.parse(phone_number)
    #     # return phonenumbers.is_valid_number_for_region(parse_number, region)
    #     return phonenumbers.is_valid_number(parse_number)
    # except:
    #     return False


def validate_price(price: [str, int, float], lowest_price: int = 1000) -> bool:
    """
    validate price
    :param price: price that you want to check
    :param lowest_price: lowest possible price
    :return: bool ==> True = price is correct
    """
    try:
        price = float(price)
        if lowest_price > price:
            return False
        return True
    except:
        return False


def validate_date(date, reg: str = "%Y-%m-%d") -> bool:
    """
    check date with its regex
    :param date: str ==> date that you want check
    :param reg: str ==> regex by example => %Y-%m-%d
    :return: bool ==> True = date is correct
    """
    try:
        if date != datetime.strptime(date, reg).strftime(reg):
            return False
        return True
    except:
        return False


def validate_time(time) -> bool:
    """
    check time with datetime
    :param time: str ==> time that you want check
    :return: bool ==> True = time is correct
    """
    try:
        datetime.strptime(time, "%H:%M")
        return True
    except:
        return False


def validate_int(value) -> bool:
    """
    check if value is numeric or not
    :param value: str or int
    :return: bool ==> True = value is numeric
    """
    return str(value).isnumeric()


def validate_float(value) -> bool:
    """
    check if value is float or not
    :param value: str or int
    :return: bool ==> True = value is float
    """
    try:
        v = float(value)
        return True
    except:
        return False


def validate_boolean(value) -> bool:
    """
    check if value is boolean or not
    :param value: str or int
    :return: bool ==> True = value is boolean
    """
    if isinstance(value, bool) or (value == "false" or value == "true"):
        return True
    return False


def validate_list(value) -> bool:
    """
    check if value is list or not
    :param value: list
    :return: bool ==> True = value is list
    """
    return isinstance(value, list)


def check_null(value_list) -> bool:
    """
    check if value list is empty or none
    :param value_list: any ==> value that you want check
    :return: bool ==> True = value list is incorrect
    """
    result_checker = []

    for data in value_list:
        if str(data).strip() == "":
            result_checker.append("an_item")

    if len(result_checker) > 0:
        return True
    return False


def check_body(value_list: [list, tuple], body: dict) -> bool:
    """
    check dict body (check if dict contains value_list keys or not)
    :param value_list: list ==> value that you want check
    :param body: list ==> dict that you want to check
    :return: bool ==> True = value list is incorrect
    """
    try:
        result = []
        if len(body.keys()) == 0:
            return True

        if type(body) is not dict:
            return True

        for value in dict(body).keys():
            if value in value_list:
                result.append(True)

        if len(result) == len(value_list) and len(value_list) == len(body.keys()):
            return False

        return True
    except:
        return True


def check_numeric(value_list: [list, tuple]) -> bool:
    """
    check if value in value_list is numeric
    :param value_list: list ==> list of value that you want check
    :return: bool ==> True = one item isn't numeric
    """
    for value in value_list:
        try:
            num = float(value)
        except:
            return True
    return False


def validate_uuid(data):
    """
    check if data is valid uuid format
    :param data: str ==> data that you wanna check
    :return: bool ==> True = uuid is right
    """
    try:
        UUID(data)
    except ValueError:
        return False
    return True


def difference_two_dates_by_minutes(date_1, date_2) -> float:
    """
    get two datetime and calc difference between its by minute
    :param date_1: datetime
    :param date_2: datetime
    :return: minutes
    """
    error_result = 9999999999999
    try:
        difference = date_1 - date_2
        result = difference.total_seconds() / 60
        return result if result > 0 else error_result
    except:
        return error_result


def validate_str_format(data: [list, tuple], check_length: bool = False) -> bool:
    """
    check if data format is string or not
    :param data: list of data
    :param check_length: check length
    :return: True => all data is string
    """
    try:
        for check_data in data:
            if type(check_data) is not str:
                return False
            if check_length and len(check_data) < 2:
                return False
        return True
    except:
        return False


def check_format(check_format: str, value: str) -> bool:
    """
    check value format
    :param check_format: format that you want
    :param value: value that you want to check
    :return: True => value format is correct, False => value format is incorrect
    """
    try:
        if check_format == "email":
            return validate_email(value)
        elif check_format == "password":
            return validate_password(value)
        elif check_format == "token":
            return validate_token(value)
        elif check_format == "text":
            return validate_text(value)
        elif check_format == "message":
            return validate_text(value, 3)
        elif check_format == "u_id":
            return validate_uid(value)
        elif check_format == "phone_number":
            return validate_phone(value, "IR")
        elif check_format == "int":
            return validate_int(value)
        elif check_format == "list":
            return validate_list(value)
        elif check_format == "float":
            return validate_float(value)
        elif check_format == "bool":
            return validate_boolean(value)
        elif check_format == "date":
            return validate_date(value, "%Y-%m-%d")
        else:
            return False
    except:
        return False


def check_full_body(body_key: list, data: dict) -> dict:
    """
    check request body and generate messages
    :param body_key: required keys, structure => [{"key": str, "required: bool, "format": str}]
    :param data: request data
    :return: status: Boolean => True is correct, message: list => list of messages
    """
    messages = []
    # --- check instance
    if not isinstance(data, dict):
        return {'status': False, "message": "request data should be an object",
                "response_status": rest_status.HTTP_400_BAD_REQUEST}
    # --- check key
    for key in body_key:
        # --- key not found
        if key['required'] and key['key'] not in list(data.keys()):
            return {'status': False, "message": "فیلد {field} یافت نشد".format(field=key['key']),
                    "response_status": rest_status.HTTP_400_BAD_REQUEST}
        # --- incorrect value
        else:
            # --- null value
            if key['required'] and data[key['key']] is None:
                return {'status': False, "message": "لطفا فیلد {field} را تکمیل کنید".format(field=key['key']),
                        "response_status": rest_status.HTTP_400_BAD_REQUEST}
            else:
                # --- invalid format
                if key['key'] in data and not key['required'] and not data[key['key']]:
                    continue
                if key['key'] in data and not check_format(key['format'], data[key['key']]):
                    return {'status': False, "message": "لطفا فیلد {field} را درست وارد کنید".format(field=key['key']),
                            "response_status": rest_status.HTTP_400_BAD_REQUEST}
    # --- response
    return {'status': True, "message": "ok", "response_status": rest_status.HTTP_200_OK}
