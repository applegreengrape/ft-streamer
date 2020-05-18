import requests
import json, time
from datetime import datetime

api = ''

def notification():
    now = datetime.now()
    now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    now = now[:-3]
    
    params = (
        ('apiKey', '{}'.format(api)),
        ('since', '{}Z'.format(now)),
    )
    
    response = requests.get('https://api.ft.com/content/notifications', params=params)
    if response.status_code == 200:
        data = json.loads(response.content)
        print(now,data)
        if data['notifications']:
            for i in data['notifications']:
                print(i['apiUrl'])

while True:
    notification()