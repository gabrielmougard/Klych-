import requests

url = 'http://localhost:5001/dump'

password = 'leubzezeh97869UYVD'

print(requests.post(url, data={'password':password}).text)