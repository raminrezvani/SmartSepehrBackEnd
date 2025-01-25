import json
from requests import request
from app_crawl.helpers import convert_gregorian_date_to_persian, ready_price
from concurrent.futures import ThreadPoolExecutor


class Sepehr360:
    def __init__(self, start_date, end_date, source, target):
        self.start_date = convert_gregorian_date_to_persian(start_date, "%Y/%m/%d")['date']
        self.end_date = convert_gregorian_date_to_persian(end_date, "%Y/%m/%d")['date']
        self.source = source
        self.target = target
        self.post_header = {
            'Content-Type': 'application/json'
        }
        self.executor = ThreadPoolExecutor(max_workers=5)

    def get_go_flight(self):
        data = json.dumps({
            "commonClientServerData": None,
            "deviceToken": "",
            "sessionId": "",
            "commonClientServerDataVersion": "",
            "currencyType": "IRR",
            "sortOrder": 1,
            "pageSize": 19,
            "pageNumber": "0",
            "isMobileWeb": False,
            "originAirportIataCode": self.source,
            "destinationAirportIataCode": self.target,
            "departureDate": self.start_date,
            "flightNumber": ""
        })
        url = "https://api.sepehr360.ir//fa/FlightAvailability/Api/B2cOnewayFlightApi/Search"
        req = request("POST", url, headers=self.post_header, data=data)
        # ---
        if req.status_code != 200:
            self.get_go_flight()
        # ---
        data = json.loads(req.text)
        result = []
        for flight in data['flightHeaderList']:
            for provider in flight['flightSupplierList']:
                try:
                    if 'listTaminKonandeganSahmiyeShenavar' in list(provider.keys()):
                        for _provider in provider['listTaminKonandeganSahmiyeShenavar']:
                            result.append({
                                "airline_name": flight['airlineName'],
                                "airline_code": flight['airlineIataCode'],
                                "go_time": flight['cleanDepartureTime'],
                                "go_date": self.start_date,
                                "return_time": flight['arrivalTime'],
                                "return_date": self.start_date,
                                "flight_number": flight['cleanFlightNumber'],
                                "provider_name": _provider['supplierName'],
                                "provider_logo": f"https://cdn.sepehr360.ir{_provider['supplierLogoUrl']}",
                                "price": int(ready_price(_provider['formattedAdultPrice'])),
                                "seat": provider['seatCount'],
                                "buy_link": f'https://sepehr360.ir/Flight/B2c/SupplierWebsiteRedirectionByRph/redirect?rph={_provider["rph"]}'
                            })
                    else:
                        result.append({
                            "airline_name": flight['airlineName'],
                            "airline_code": flight['airlineIataCode'],
                            "go_time": flight['cleanDepartureTime'],
                            "go_date": self.start_date,
                            "return_time": flight['arrivalTime'],
                            "return_date": self.start_date,
                            "flight_number": flight['cleanFlightNumber'],
                            "provider_name": provider['supplierName'],
                            "provider_logo": f"https://cdn.sepehr360.ir{provider['supplierLogoUrl']}",
                            "price": int(ready_price(provider['formattedAdultPrice'])),
                            "seat": provider['seatCount'],
                            "buy_link": f'https://sepehr360.ir/Flight/B2c/SupplierWebsiteRedirectionByRph/redirect?rph={provider["rph"]}'
                        })
                except KeyError:
                    continue
        # ---
        return result

    def get_return_flight(self):
        data = json.dumps({
            "commonClientServerData": None,
            "deviceToken": "",
            "sessionId": "",
            "commonClientServerDataVersion": "",
            "currencyType": "IRR",
            "sortOrder": 1,
            "pageSize": 19,
            "pageNumber": "0",
            "isMobileWeb": False,
            "originAirportIataCode": self.target,
            "destinationAirportIataCode": self.source,
            "departureDate": self.end_date,
            "flightNumber": ""
        })
        url = "https://api.sepehr360.ir//fa/FlightAvailability/Api/B2cOnewayFlightApi/Search"
        req = request("POST", url, headers=self.post_header, data=data)
        # ---
        if req.status_code != 200:
            self.get_return_flight()
        # ---
        data = json.loads(req.text)
        result = []
        for flight in data['flightHeaderList']:
            for provider in flight['flightSupplierList']:
                try:
                    if 'listTaminKonandeganSahmiyeShenavar' in list(provider.keys()):
                        for _provider in provider['listTaminKonandeganSahmiyeShenavar']:
                            result.append({
                                "airline_name": flight['airlineName'],
                                "airline_code": flight['airlineIataCode'],
                                "go_time": flight['cleanDepartureTime'],
                                "go_date": self.end_date,
                                "return_time": flight['arrivalTime'],
                                "return_date": self.end_date,
                                "flight_number": flight['cleanFlightNumber'],
                                "provider_name": _provider['supplierName'],
                                "provider_logo": f"https://cdn.sepehr360.ir{_provider['supplierLogoUrl']}",
                                "price": int(ready_price(_provider['formattedAdultPrice'])),
                                "seat": provider['seatCount'],
                                "buy_link": f'https://sepehr360.ir/Flight/B2c/SupplierWebsiteRedirectionByRph/redirect?rph={_provider["rph"]}'
                            })
                    else:
                        result.append({
                            "airline_name": flight['airlineName'],
                            "airline_code": flight['airlineIataCode'],
                            "go_time": flight['cleanDepartureTime'],
                            "go_date": self.end_date,
                            "return_time": flight['arrivalTime'],
                            "return_date": self.end_date,
                            "flight_number": flight['cleanFlightNumber'],
                            "provider_name": provider['supplierName'],
                            "provider_logo": f"https://cdn.sepehr360.ir{provider['supplierLogoUrl']}",
                            "price": int(ready_price(provider['formattedAdultPrice'])),
                            "seat": provider['seatCount'],
                            "buy_link": f'https://sepehr360.ir/Flight/B2c/SupplierWebsiteRedirectionByRph/redirect?rph={provider["rph"]}'
                        })
                except KeyError:
                    continue
        # ---
        return result

    def get_result(self, one_way=True):
        try:
            result = dict()
            go_flight = self.executor.submit(self.get_go_flight)
            if not one_way:
                return_flight = self.executor.submit(self.get_return_flight)
                result['go_flight'] = go_flight.result()
                result['return_flight'] = return_flight.result()
            else:
                result = go_flight.result()
            # ---
            return result
        except:
            return {"go_flight": [], "return_flight": []} if not one_way else []

# sepehr = Sepehr360("2023-01-29", "2023-02-06", "MHD", "KIH")
# print("--------------------------------")
# print(sepehr.get_result())
