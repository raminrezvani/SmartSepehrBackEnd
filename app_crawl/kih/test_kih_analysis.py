import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'JWT eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyOTk5ODI5LCJpYXQiOjE3NDI4MjcwMjksImp0aSI6ImI2YzI1NzFkMGI0MTQxZmY5OGUwMTZhMzVkMjRiZDliIiwidXNlcl9pZCI6MTN9.2XN--WgzgHT_QLkdVfXfd9j4x0HujMb294CK4txEanmtJcN7nrYH1-K0Z9M2GJKyaN2ky2sEEX7gJ-DmzAwW-A',
    'content-type': 'application/json',
    'origin': 'https://tour-collector.sepehrsmart.ir',
    'priority': 'u=1, i',
    'referer': 'https://tour-collector.sepehrsmart.ir/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

json_data = {
    'source': 'MHD',
    'target': 'KIH',
    'start_date': '2025-04-07',
    'night_count': 3,
    'range_number': 7,
    'adults': 2,
    'use_cache': True,
}

response = requests.post('http://localhost:8765/get-analysis/', headers=headers, json=json_data)
print(response.text)