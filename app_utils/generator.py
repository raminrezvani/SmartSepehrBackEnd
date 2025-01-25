import random
import string
import uuid
from datetime import datetime


def generate_random_token() -> int:
    """
    generate random token
    :return: int ==> token, length => 5
    """
    return 11111
    # token = datetime.now().strftime("%f")[-5:]
    # # ---
    # if len(token) != 5:
    #     generate_random_token()
    # # ---
    # return int(token)


def generate_random_string(size: int = 6, upper_case=True, digits=True, lower_case=True) -> str:
    """
    random string generator
    :param size: int ==> wanted string length
    :param upper_case: your string contains upper case words
    :param digits: your string contains digits
    :param lower_case: your string contains lower case words
    :return: str ==> random text
    """
    chars = ''
    # chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    if upper_case:
        chars += string.ascii_uppercase
    if digits:
        chars += string.digits
    if lower_case:
        chars += string.ascii_lowercase
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def generate_unique_id() -> int:
    """
    generate a number id
    :return: int with 13 digits
    """
    date = datetime.now()
    year = date.strftime("%Y")[-2:]
    day = date.strftime("%j")
    hour = date.strftime("%H")
    minute = date.strftime("%M")
    second = date.strftime("%S")
    result = f"{year}{day}{hour}{minute}{second}{random.SystemRandom().randint(10, 99)}"
    return int(result)


def generate_unique_u_id() -> str:
    """
    generate random u_id (uuid)
    :return: unique u_id
    """
    # --- u_id 1
    random_u_id_1 = uuid.uuid4().hex
    random_u_id_2 = uuid.uuid1().hex
    u_id_text_1 = f"{random_u_id_1}_{generate_random_token()}_{random_u_id_2}_{generate_random_string()}"
    u_id_1 = uuid.uuid5(uuid.NAMESPACE_DNS, u_id_text_1)
    # --- u_id 2
    random_u_id_1 = uuid.uuid1().hex
    random_u_id_2 = uuid.uuid4().hex
    u_id_text_2 = f"{random_u_id_2}_{u_id_1}_{random_u_id_1}_{generate_unique_id()}_{generate_random_string()}"
    u_id_2 = uuid.uuid3(uuid.NAMESPACE_DNS, u_id_text_2)
    # --- finally
    unique_id = str(generate_unique_id())
    return f'J-{unique_id[:8]}-{uuid.uuid5(uuid.NAMESPACE_DNS, f"{u_id_1}_{u_id_2}")}-{unique_id[8:]}-J'
