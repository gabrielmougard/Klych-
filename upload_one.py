import requests
import sys

filename = sys.argv[1]


auth = {'password':'leubzezeh97869UYVD'}
data = open(filename, 'rb')
# api_url = 'http://localhost:5001/upload'
api_url = 'https://home.plawn-inc.science/face/api/upload'
r = requests.post(api_url, data=auth, files={'file':data})

print(r.text)