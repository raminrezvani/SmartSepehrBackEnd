import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'JWT eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1MzMxNTYwLCJpYXQiOjE3NDUxNTg3NjAsImp0aSI6ImMzNmVlYjNmYzU5NzQ3MzA4NTExMTdmM2ExYjMxYWIyIiwidXNlcl9pZCI6MTN9.aJpgDVraOjXa5owoYjGa_7Nwo2Cs7ws1NmzZKdy1ZCBPHhnQVl5iH6Nc2eoZYtgD1swKVRk5W-6xqNJCq9BwJQ',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://127.0.0.1:8080',
    'Referer': 'http://127.0.0.1:8080/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'start_date': '2025-04-24',
    'end_date': '2025-04-28',
    'night_count': 4,
    'hotel_star': 5,
    'source': 'asdsa',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
}

response = requests.post('http://127.0.0.1:8765/build-tour/', headers=headers, json=json_data)
print(response.text)



