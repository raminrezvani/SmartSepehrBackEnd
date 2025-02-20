import requests

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Authorization': 'JWT eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMDcyMzczLCJpYXQiOjE3Mzk4OTk1NzMsImp0aSI6IjE3YTMyMzUxOTJhNTQyYjU5MTMyOTM1MmUwMjg3YWY3IiwidXNlcl9pZCI6MTN9.GkHWBhLavh0kGALns1GIouTHB1_ctybZTLZ4ooRZJ2UpS-NVx2CuSBUmfpk_3BppqPqM9mb61n_cvQKzP-q6Ag',
    'Referer': 'http://localhost:8080/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
}

json_data = {
    'start_date': '2025-03-17',
    'end_date': '2025-03-21',
    'night_count': 4,
    'hotel_star': 5,
    'source': 'THR',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
    'hotelstarAnalysis': [
        '5',
    ],
}
def req_to_hotels():
    res=requests.post('http://127.0.0.1:8765/build-tour-analyse/', headers=headers, json=json_data)
    return res
from concurrent.futures import ThreadPoolExecutor,as_completed
futures=[]
import time
with ThreadPoolExecutor(max_workers=30) as executor:
    for i in range(0,1):
        futures.append(executor.submit(req_to_hotels))
        time.sleep(1)
    for future in as_completed(futures):
        future.result()

