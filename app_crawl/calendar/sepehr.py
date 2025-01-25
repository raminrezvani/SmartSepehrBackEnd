import json

from requests import request
import jdatetime
from datetime import date
from dateutil.relativedelta import relativedelta


class SepehrCalendar:
    def __init__(self, source, target, skip_month=0):
        georgian_date = date.today() + relativedelta(months=skip_month)
        self.source = source
        self.target = target
        self.start_date = jdatetime.date.fromgregorian(day=georgian_date.day, month=georgian_date.month,
                                                       year=georgian_date.year)

    def get_data(self, source, target) -> dict:
        try:
            req_url = "https://api.sepehr360.ir//fa/FlightAvailability/Api/CalendarPricesApi/Get"

            params = {
                "Source": source,
                "Destination": target,
                "SelectedDate": self.start_date,
                "CurrencyType": "IRR"
            }

            req = request("GET", req_url, params=params)

            return json.loads(req.text)
        except:
            return {}

    def get_result(self):
        go_data = self.get_data(source=self.source, target=self.target)
        return_data = self.get_data(source=self.target, target=self.source)

        return {
            "go": go_data.get("arrival", []),
            "return": return_data.get("arrival", []),
        }
