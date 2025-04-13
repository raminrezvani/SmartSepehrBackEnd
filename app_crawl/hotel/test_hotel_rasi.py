import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'JWT eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NzEwMjAyLCJpYXQiOjE3NDQ1Mzc0MDIsImp0aSI6ImExNTVjZTFiYmIyNjRiMGZiMTQyZDcwMGQyYTZkMWVjIiwidXNlcl9pZCI6MTN9.E-redMcrchfQfamWgo6wb4HJ-2W29jBETm5ucFCWrmO2SSbH4yLSljLjdwwghQYMmR9Gr3KTwCJmLsQYISNE1w',
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
    'start_date': '2025-04-20',
    'end_date': '2025-04-24',
    'night_count': 4,
    'hotel_star': 5,
    'source': 'asdsa',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
}

response = requests.post('http://127.0.0.1:8765/build-tour/', headers=headers, json=json_data)
print(response.text)



