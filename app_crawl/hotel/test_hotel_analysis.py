# import requests
#
# headers = {
#     'sec-ch-ua-platform': '"Windows"',
#     'Authorization': 'JWT eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQzNDE4Njk1LCJpYXQiOjE3NDMyNDU4OTUsImp0aSI6IjQ0ZjFmNWMyNzlhNDQ5MzNiMTc4NWI4NjY1NjI2Mjg2IiwidXNlcl9pZCI6MTN9.O_yujJSHZ-Yiw5txNOONuJklVLfOD6e_K5WrmQxrEyNtggy_5F7Byb0EjiwlLLbrm22tvLHNL4Ny1J-VhosYxw',
#     'Referer': 'http://localhost:8080/',
#     'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
#     'sec-ch-ua-mobile': '?0',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
#     'Accept': 'application/json, text/plain, */*',
#     'Content-Type': 'application/json',
# }
#
# json_data = {
#     'start_date': '2025-04-12',
#     'end_date': '2025-04-15',
#     'night_count': 3,
#     'hotel_star': 5,
#     'source': 'THR',
#     'target': 'KIH',
#     'adults': 2,
#     'use_cache': False,
#     'range': 7,
#     # 'hotelstarAnalysis': [
#     #     '5',
#     # ],
#     'hotelstarAnalysis': [
#         'هتل پانوراما کيش',
#         'هتل پارميس کيش',
#         'هتل بين المللی کيش'
#     ],
#
# }
#
# response = requests.post('http://127.0.0.1:8765/build-tour-analyse/', headers=headers, json=json_data)
# import json
# aa=json.loads(response.text)
# print('asd')



import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'JWT eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQzNTQyMDYwLCJpYXQiOjE3NDMzNjkyNjAsImp0aSI6ImI2ZjEwNDJkMTA3ZTQ5ZThiYTM4MTA0MDY5MjcwOGI1IiwidXNlcl9pZCI6MTN9.EMiozDb9nj9DfAoUS1anIqsxP_qXM8h1irqIqIULt7fxfHhtvAMrgalibcqToef4k77jqQrYhhMWQS47q_0xog',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:8080',
    'Referer': 'http://localhost:8080/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'start_date': '2025-04-13',
    'end_date': '2025-04-16',
    'night_count': 3,
    'hotel_star': 5,
    'source': 'MHD',
    'target': 'KIH',
    'adults': 2,
    'use_cache': False,
    'hotelstarAnalysis': [
        'هتل پانوراما کيش',
    ],
    'range': 7,
}

#
# json_data = {
#     'start_date': '2025-04-12',
#     'end_date': '2025-04-15',
#     'night_count': 3,
#     'hotel_star': 5,
#     'source': 'THR',
#     'target': 'KIH',
#     'adults': 2,
#     'use_cache': False,
#     'range': 7,
#     # 'hotelstarAnalysis': [
#     #     '5',
#     # ],
#     'hotelstarAnalysis': [
#         'هتل پانوراما کيش',
#         'هتل پارميس کيش',
#         'هتل بين المللی کيش'
#     ],
# }



response = requests.post('http://127.0.0.1:8765/build-tour-analyse/', headers=headers, json=json_data)


import json
aa=json.loads(response.text)
print('asd')