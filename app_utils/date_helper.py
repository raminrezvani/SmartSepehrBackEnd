import datetime

import pytz


def get_current_time():
    """
    get current time
    :return: datetime instance
    """
    # return datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
    return datetime.datetime.now(pytz.timezone("UTC"))
