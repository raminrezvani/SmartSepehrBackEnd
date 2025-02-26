import requests
import json
headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Authorization': 'JWT eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNjczNzkyLCJpYXQiOjE3NDA1MDA5OTIsImp0aSI6IjU1OGE2ZTM3ZjIzNTRmZWZiOGRkZmE2NWNmNzczYTJhIiwidXNlcl9pZCI6MTN9.E0hY6bhyKuBYMgDTVooeKCu5OTQSyQ2t8KIEUbSDUp3hv9irwa-XZ042R5MZU_Ht8NEUasGY5hjh1exlPfSXMw',
    'Referer': 'http://localhost:8080/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
}

json_data_1 = {
    'start_date': '2025-03-10',
    'end_date': '2025-03-13',
    'night_count': 3,
    'hotel_star': 5,
    'source': 'TBZ',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
    'hotelstarAnalysis': [
        '5',
    ],
}
json_data_2 = {
    'start_date': '2025-03-10',
    'end_date': '2025-03-13',
    'night_count': 3,
    'hotel_star': 5,
    'source': 'MHD',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
    'hotelstarAnalysis': [
        '5',
    ],
}
json_data_3 = {
    'start_date': '2025-03-10',
    'end_date': '2025-03-13',
    'night_count': 3,
    'hotel_star': 5,
    'source': 'THR',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
    'hotelstarAnalysis': [
        '5',
    ],
}
json_data_4 = {
    'start_date': '2025-03-10',
    'end_date': '2025-03-13',
    'night_count': 3,
    'hotel_star': 5,
    'source': 'SYZ',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
    'hotelstarAnalysis': [
        '5',
    ],
}


def req_to_hotels(json_data):
    res=requests.post('http://127.0.0.1:8765/build-tour-analyse/', headers=headers, json=json_data)
    return res
from concurrent.futures import ThreadPoolExecutor,as_completed
futures=[]
import time
with ThreadPoolExecutor(max_workers=30) as executor:
    futures.append(executor.submit(req_to_hotels,json_data_1))
    time.sleep(10)
    futures.append(executor.submit(req_to_hotels,json_data_2))
    time.sleep(10)
    futures.append(executor.submit(req_to_hotels,json_data_3))
    time.sleep(10)
    # # futures.append(executor.submit(req_to_hotels,json_data_4))


    # for i in range(0,20):
    #     futures.append(executor.submit(req_to_hotels))
    #     time.sleep(5)

    for future in as_completed(futures):
        res=future.result()
        print(f'result=== {res.status_code}')
              # f'data=== {len(json.loads(res.text)["2025-03-24"]["hotel"])}')
              # f'data=== {len((res.text]['hotel'])}')

        # Dictionary to store the count of hotels per provider
        provider_hotel_count = {}
        # Iterate over each date in the data
        for date, info in json.loads(res.text).items():
            hotels = info.get('hotel', [])
            for hotel in hotels:
                provider = hotel.get('provider')
                if provider:
                    if provider not in provider_hotel_count:
                        provider_hotel_count[provider] = 0
                    provider_hotel_count[provider] += 1

        # Print the results
        for provider, count in provider_hotel_count.items():
            print(f"Provider: {provider}, Hotel Count: {count}")

